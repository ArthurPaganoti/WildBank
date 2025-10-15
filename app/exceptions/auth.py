from typing import Any, Dict, Optional
from .base import AppException


class AuthenticationException(AppException):

    def __init__(
            self,
            message: str = "Falha na autenticação",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTH_FAILED",
            details=details
        )


class InvalidCredentialsException(AuthenticationException):

    def __init__(self, message: str = "E-mail ou senha inválidos"):
        super().__init__(
            message=message,
            details={"hint": "Verifique suas credenciais e tente novamente"}
        )
        self.error_code = "INVALID_CREDENTIALS"


class TokenExpiredException(AuthenticationException):

    def __init__(self, message: str = "Token expirado. Faça login novamente"):
        super().__init__(
            message=message,
            details={"hint": "Utilize o refresh token ou faça login novamente"}
        )
        self.error_code = "TOKEN_EXPIRED"


class InvalidTokenException(AuthenticationException):

    def __init__(self, message: str = "Token inválido"):
        super().__init__(
            message=message,
            details={"hint": "Token inválido ou malformado"}
        )
        self.error_code = "INVALID_TOKEN"


class RefreshTokenExpiredException(AuthenticationException):

    def __init__(self, message: str = "Refresh token expirado. Faça login novamente"):
        super().__init__(
            message=message,
            details={"hint": "Seu refresh token expirou, é necessário fazer login novamente"}
        )
        self.error_code = "REFRESH_TOKEN_EXPIRED"


class UnauthorizedException(AppException):

    def __init__(
            self,
            message: str = "Você não tem permissão para acessar este recurso",
            resource: Optional[str] = None
    ):
        details = {}
        if resource:
            details["resource"] = resource

        super().__init__(
            message=message,
            status_code=403,
            error_code="UNAUTHORIZED",
            details=details
        )


class MissingTokenException(AuthenticationException):

    def __init__(self, message: str = "Token de autenticação não fornecido"):
        super().__init__(
            message=message,
            details={"hint": "Inclua o token no header Authorization"}
        )
        self.error_code = "MISSING_TOKEN"

