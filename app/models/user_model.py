from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import datetime, timezone
from typing import Optional

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    sobrenome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(500), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)

    cep: Mapped[str] = mapped_column(String(500), nullable=False)
    logradouro: Mapped[str] = mapped_column(String(500), nullable=False)
    numero: Mapped[str] = mapped_column(String(500), nullable=False)
    complemento: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bairro: Mapped[str] = mapped_column(String(500), nullable=False)
    cidade: Mapped[str] = mapped_column(String(500), nullable=False)
    estado: Mapped[str] = mapped_column(String(500), nullable=False)

    refresh_token: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    refresh_token_expires: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    password_reset_token: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    password_reset_expires: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, nome={self.nome}, sobrenome={self.sobrenome}, cpf={self.cpf})>"
