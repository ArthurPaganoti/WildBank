from typing import Optional
from .base import AppException


class DatabaseException(AppException):

    def __init__(
            self,
            message: str = "Erro ao acessar banco de dados",
            original_error: Optional[str] = None,
            operation: Optional[str] = None
    ):
        details = {}
        if original_error:
            details["original_error"] = str(original_error)
        if operation:
            details["operation"] = operation

        super().__init__(
            message=message,
            status_code=500,
            error_code="DATABASE_ERROR",
            details=details
        )


class CacheException(AppException):

    def __init__(
            self,
            message: str = "Erro ao acessar cache",
            original_error: Optional[str] = None,
            operation: Optional[str] = None
    ):
        details = {}
        if original_error:
            details["original_error"] = str(original_error)
        if operation:
            details["operation"] = operation

        super().__init__(
            message=message,
            status_code=500,
            error_code="CACHE_ERROR",
            details=details
        )


class ExternalServiceException(AppException):

    def __init__(
            self,
            service: str,
            message: str = "Erro ao comunicar com serviço externo",
            original_error: Optional[str] = None
    ):
        details = {"service": service}
        if original_error:
            details["original_error"] = str(original_error)

        super().__init__(
            message=message,
            status_code=503,
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details
        )


class ViaCEPException(ExternalServiceException):

    def __init__(
            self,
            cep: str,
            message: str = "Erro ao consultar CEP",
            original_error: Optional[str] = None
    ):
        super().__init__(
            service="ViaCEP",
            message=message,
            original_error=original_error
        )
        self.details["cep"] = cep
        self.error_code = "VIACEP_ERROR"


class RateLimitException(AppException):

    def __init__(
            self,
            message: str = "Muitas requisições. Tente novamente mais tarde",
            retry_after: Optional[int] = None,
            limit: Optional[str] = None
    ):
        details = {}
        if retry_after:
            details["retry_after"] = retry_after
        if limit:
            details["limit"] = limit

        super().__init__(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
            details=details
        )


class EncryptionException(AppException):

    def __init__(
            self,
            message: str = "Erro ao processar dados criptografados",
            operation: Optional[str] = None
    ):
        details = {}
        if operation:
            details["operation"] = operation

        super().__init__(
            message=message,
            status_code=500,
            error_code="ENCRYPTION_ERROR",
            details=details
        )


class ConfigurationException(AppException):

    def __init__(
            self,
            message: str = "Erro de configuração da aplicação",
            config_key: Optional[str] = None
    ):
        details = {}
        if config_key:
            details["config_key"] = config_key

        super().__init__(
            message=message,
            status_code=500,
            error_code="CONFIGURATION_ERROR",
            details=details
        )


"""
Sistema de exceções customizadas para padronizar tratamento de erros.
"""
from .base import AppException
from .auth import (
    AuthenticationException,
    InvalidCredentialsException,
    TokenExpiredException,
    InvalidTokenException,
    UnauthorizedException
)
from .resource import (
    NotFoundException,
    UserNotFoundException
)
from .validation import (
    ValidationException,
    DuplicateResourceException,
    EmailAlreadyExistsException,
    CPFAlreadyExistsException,
    InvalidCPFException,
    InvalidPasswordException
)
from .business import (
    BusinessRuleException,
    PasswordResetException
)
from .system import (
    DatabaseException,
    CacheException,
    ExternalServiceException,
    RateLimitException
)

__all__ = [
    "AppException",

    "AuthenticationException",
    "InvalidCredentialsException",
    "TokenExpiredException",
    "InvalidTokenException",
    "UnauthorizedException",

    "NotFoundException",
    "UserNotFoundException",

    "ValidationException",
    "DuplicateResourceException",
    "EmailAlreadyExistsException",
    "CPFAlreadyExistsException",
    "InvalidCPFException",
    "InvalidPasswordException",

    "BusinessRuleException",
    "PasswordResetException",

    "DatabaseException",
    "CacheException",
    "ExternalServiceException",
    "RateLimitException",
]

