from .base import AppException
from .auth import (
    AuthenticationException,
    InvalidCredentialsException,
    TokenExpiredException,
    InvalidTokenException,
    RefreshTokenExpiredException,
    UnauthorizedException,
    MissingTokenException
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
    InvalidPasswordException,
    InvalidEmailFormatException,
    InvalidCEPException
)
from .bussines import (
    BusinessRuleException,
    PasswordResetException,
    PasswordResetTokenExpiredException,
    InvalidPasswordResetTokenException,
    SelfDeletionException,
    UnauthorizedAccountAccessException
)
from .system import (
    DatabaseException,
    CacheException,
    ExternalServiceException,
    ViaCEPException,
    RateLimitException,
    EncryptionException,
    ConfigurationException
)

__all__ = [
    "AppException",
    # Auth
    "AuthenticationException",
    "InvalidCredentialsException",
    "TokenExpiredException",
    "InvalidTokenException",
    "RefreshTokenExpiredException",
    "UnauthorizedException",
    "MissingTokenException",
    "NotFoundException",
    "UserNotFoundException",
    "ValidationException",
    "DuplicateResourceException",
    "EmailAlreadyExistsException",
    "CPFAlreadyExistsException",
    "InvalidCPFException",
    "InvalidPasswordException",
    "InvalidEmailFormatException",
    "InvalidCEPException",
    "BusinessRuleException",
    "PasswordResetException",
    "PasswordResetTokenExpiredException",
    "InvalidPasswordResetTokenException",
    "SelfDeletionException",
    "UnauthorizedAccountAccessException",
    "DatabaseException",
    "CacheException",
    "ExternalServiceException",
    "ViaCEPException",
    "RateLimitException",
    "EncryptionException",
    "ConfigurationException",
]
