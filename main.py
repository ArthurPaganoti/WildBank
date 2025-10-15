from fastapi import FastAPI
from app.routers import user_router
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.core.logging import setup_logging, get_logger
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy.exc import SQLAlchemyError
from redis.exceptions import RedisError

from app.exceptions import AppException
from app.exceptions.handlers import (
    app_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    redis_exception_handler,
    generic_exception_handler
)

setup_logging()
logger = get_logger(__name__)

if settings.sentry_dsn:
    import sentry_sdk
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        traces_sample_rate=1.0 if settings.environment == "development" else 0.1,
    )
    logger.info("sentry_initialized", environment=settings.environment)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("application_startup", environment=settings.environment)
    await init_db()
    logger.info("database_initialized")
    yield
    logger.info("application_shutdown")

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Wild Bank",
    description="""
    ## WildBank API

    Bem-vindo à API oficial do WildBank!

    O WildBank é uma plataforma digital inovadora para gestão bancária, oferecendo segurança, performance e praticidade para usuários e desenvolvedores. Esta API faz parte da infraestrutura do WildBank, permitindo o gerenciamento seguro de contas, autenticação de usuários, operações financeiras e integração com serviços essenciais.

    ### Documentação Completa

    Consulte [API_DOCUMENTATION.md](https://github.com/ArthurPaganoti/WildBank/API_DOCUMENTATION.md) para um guia detalhado de integração e uso.
    """,
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Suporte",
        "email": "paganotiarthur@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {
            "name": "users",
            "description": "Operações com usuários - registro, autenticação, gerenciamento",
        },
        {
            "name": "health",
            "description": "Health checks e status da aplicação",
        }
    ]
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(RedisError, redis_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)

@app.get("/")
async def root():
    return {
        "message": "API de autenticação está funcionando com PostgreSQL!",
        "version": "2.0.0",
        "features": [
            "JWT Authentication",
            "Refresh Tokens",
            "Structured Logging",
            "Rate Limiting",
            "Data Encryption (LGPD compliant)",
            "Audit Timestamps"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "2.0.0"
    }
