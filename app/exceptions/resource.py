from typing import Any, Optional
from .base import AppException


class NotFoundException(AppException):

    def __init__(
            self,
            resource: str = "Recurso",
            resource_id: Optional[Any] = None,
            message: Optional[str] = None
    ):
        if message is None:
            message = f"{resource} não encontrado"
            if resource_id:
                message += f" (ID: {resource_id})"

        details = {"resource": resource}
        if resource_id:
            details["resource_id"] = resource_id

        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND",
            details=details
        )


class UserNotFoundException(NotFoundException):

    def __init__(
            self,
            user_id: Optional[int] = None,
            email: Optional[str] = None,
            message: Optional[str] = None
    ):
        if message is None:
            message = "Usuário não encontrado"

        details = {}
        if user_id:
            details["user_id"] = user_id
        if email:
            details["email"] = email

        super().__init__(
            resource="Usuário",
            resource_id=user_id,
            message=message
        )
        self.details.update(details)
        self.error_code = "USER_NOT_FOUND"

