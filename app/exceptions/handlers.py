from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from redis.exceptions import RedisError
from app.exceptions import AppException
from app.core.logging import get_logger
import traceback

logger = get_logger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    logger.warning(
        "app_exception",
        error_code=exc.error_code,
        status_code=exc.status_code,
        message=exc.message,
        path=request.url.path,
        method=request.method,
        details=exc.details
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(
        "validation_error",
        path=request.url.path,
        method=request.method,
        errors=errors
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Erro de validação nos dados enviados",
                "code": "VALIDATION_ERROR",
                "status_code": 422,
                "details": {
                    "errors": errors
                }
            }
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.error(
        "database_error",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        traceback=traceback.format_exc()
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Erro ao acessar banco de dados",
                "code": "DATABASE_ERROR",
                "status_code": 500,
                "details": {}
            }
        }
    )


async def redis_exception_handler(request: Request, exc: RedisError) -> JSONResponse:
    logger.error(
        "cache_error",
        path=request.url.path,
        method=request.method,
        error=str(exc)
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Erro temporário no sistema de cache",
                "code": "CACHE_ERROR",
                "status_code": 500,
                "details": {
                    "hint": "A operação pode ser mais lenta que o normal"
                }
            }
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        error_type=type(exc).__name__,
        traceback=traceback.format_exc()
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Erro interno do servidor",
                "code": "INTERNAL_ERROR",
                "status_code": 500,
                "details": {
                    "hint": "Um erro inesperado ocorreu. Entre em contato com o suporte se o problema persistir"
                }
            }
        }
    )

