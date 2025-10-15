from typing import Any, Dict, Optional


class AppException(Exception):

    def __init__(
            self,
            message: str,
            status_code: int = 500,
            error_code: str = "INTERNAL_ERROR",
            details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": {
                "message": self.message,
                "code": self.error_code,
                "status_code": self.status_code,
                "details": self.details
            }
        }

    def __str__(self) -> str:
        return f"{self.error_code}: {self.message}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(code={self.error_code}, status={self.status_code})>"

