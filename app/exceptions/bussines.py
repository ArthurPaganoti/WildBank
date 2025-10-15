from typing import Any, Dict, Optional
from .base import AppException


class BusinessRuleException(AppException):

    def __init__(
            self,
            message: str,
            rule: str,
            details: Optional[Dict[str, Any]] = None
    ):
        error_details = details or {}
        error_details["rule"] = rule

        super().__init__(
            message=message,
            status_code=400,
            error_code="BUSINESS_RULE_VIOLATION",
            details=error_details
        )


class PasswordResetException(BusinessRuleException):

    def __init__(
            self,
            message: str = "Erro ao processar reset de senha",
            reason: Optional[str] = None
    ):
        details = {}
        if reason:
            details["reason"] = reason

        super().__init__(
            message=message,
            rule="password_reset",
            details=details
        )
        self.error_code = "PASSWORD_RESET_ERROR"


class PasswordResetTokenExpiredException(PasswordResetException):

    def __init__(self):
        super().__init__(
            message="Token de reset de senha expirado. Solicite um novo reset",
            reason="token_expired"
        )
        self.error_code = "PASSWORD_RESET_TOKEN_EXPIRED"


class InvalidPasswordResetTokenException(PasswordResetException):

    def __init__(self):
        super().__init__(
            message="Token de reset de senha inválido",
            reason="invalid_token"
        )
        self.error_code = "INVALID_PASSWORD_RESET_TOKEN"


class SelfDeletionException(BusinessRuleException):

    def __init__(self):
        super().__init__(
            message="Você não pode deletar sua própria conta",
            rule="self_deletion_forbidden"
        )
        self.error_code = "SELF_DELETION_FORBIDDEN"


class UnauthorizedAccountAccessException(BusinessRuleException):

    def __init__(self, action: str = "acessar"):
        super().__init__(
            message=f"Você só pode {action} sua própria conta",
            rule="own_account_only",
            details={"action": action}
        )
        self.error_code = "UNAUTHORIZED_ACCOUNT_ACCESS"

