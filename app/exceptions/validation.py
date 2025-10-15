from typing import Any, Dict, Optional
from .base import AppException


class ValidationException(AppException):

    def __init__(
            self,
            message: str,
            field: Optional[str] = None,
            details: Optional[Dict[str, Any]] = None
    ):
        error_details = details or {}
        if field:
            error_details["field"] = field

        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=error_details
        )


class DuplicateResourceException(AppException):

    def __init__(
            self,
            resource: str,
            field: str,
            value: Any,
            message: Optional[str] = None
    ):
        if message is None:
            message = f"{resource} com {field} '{value}' já existe"

        super().__init__(
            message=message,
            status_code=409,
            error_code="DUPLICATE_RESOURCE",
            details={
                "resource": resource,
                "field": field,
                "value": value
            }
        )


class EmailAlreadyExistsException(DuplicateResourceException):

    def __init__(self, email: str):
        super().__init__(
            resource="Usuário",
            field="e-mail",
            value=email,
            message="E-mail já cadastrado"
        )
        self.error_code = "EMAIL_ALREADY_EXISTS"


class CPFAlreadyExistsException(DuplicateResourceException):

    def __init__(self, cpf: str):
        masked_cpf = f"{cpf[:3]}***{cpf[-2:]}" if len(cpf) >= 5 else "***"
        super().__init__(
            resource="Usuário",
            field="CPF",
            value=masked_cpf,
            message="CPF já cadastrado"
        )
        self.error_code = "CPF_ALREADY_EXISTS"


class InvalidCPFException(ValidationException):

    def __init__(self, message: str = "CPF inválido"):
        super().__init__(
            message=message,
            field="cpf",
            details={"hint": "Verifique se o CPF está correto"}
        )
        self.error_code = "INVALID_CPF"


class InvalidPasswordException(ValidationException):

    def __init__(
            self,
            message: str = "Senha não atende aos requisitos de segurança",
            requirements: Optional[Dict[str, bool]] = None
    ):
        details = {"hint": "A senha deve ter no mínimo 8 caracteres"}
        if requirements:
            details["requirements"] = requirements

        super().__init__(
            message=message,
            field="senha",
            details=details
        )
        self.error_code = "INVALID_PASSWORD"


class InvalidEmailFormatException(ValidationException):

    def __init__(self, email: str):
        super().__init__(
            message=f"Formato de e-mail inválido: {email}",
            field="email",
            details={"hint": "Verifique se o e-mail está no formato correto"}
        )
        self.error_code = "INVALID_EMAIL_FORMAT"


class InvalidCEPException(ValidationException):

    def __init__(self, message: str = "CEP inválido"):
        super().__init__(
            message=message,
            field="cep",
            details={"hint": "CEP deve conter 8 dígitos"}
        )
        self.error_code = "INVALID_CEP"

