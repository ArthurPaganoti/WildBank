from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: str = os.getenv("POSTGRES_PORT", "5432")
    postgres_db: str = os.getenv("POSTGRES_DB", "fastapi_db")

    @property
    def database_url(self) -> str:
        if self.postgres_password:
            return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        else:
            return f"postgresql+asyncpg://{self.postgres_user}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    secret_key: str = os.getenv("SECRET_KEY", "")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    sentry_dsn: str = os.getenv("SENTRY_DSN", "")
    environment: str = os.getenv("ENVIRONMENT", "development")

    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    backend_url: str = os.getenv("BACKEND_URL", "http://localhost:8000")

    allowed_origins: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
    redis_password: str = os.getenv("REDIS_PASSWORD", "")
    redis_db: int = int(os.getenv("REDIS_DB", "0"))
    redis_url: str = os.getenv("REDIS_URL", "")

    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: str = os.getenv("SMTP_USERNAME", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email: str = os.getenv("SMTP_FROM_EMAIL", "")
    smtp_from_name: str = os.getenv("SMTP_FROM_NAME", "FastAPI App")
    smtp_tls: bool = os.getenv("SMTP_TLS", "true").lower() == "true"
    smtp_ssl: bool = os.getenv("SMTP_SSL", "false").lower() == "true"

    password_reset_expire_hours: int = int(os.getenv("PASSWORD_RESET_EXPIRE_HOURS", "1"))

    class Config:
        case_sensitive = False

    def validate_settings(self):
        if not self.secret_key or self.secret_key == "":
            raise ValueError(
                "SECRET_KEY não está definida! "
                "Execute: openssl rand -hex 32 "
                "e adicione ao arquivo .env"
            )

settings = Settings()
settings.validate_settings()
