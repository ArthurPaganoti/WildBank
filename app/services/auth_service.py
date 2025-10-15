from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_refresh_token, \
    hash_password
from app.schemas.user_schema import UserResponse
from app.core.logging import get_logger
from datetime import datetime, timezone, timedelta
from app.core.config import settings
from app.exceptions import (
    InvalidCredentialsException,
    UserNotFoundException,
    InvalidTokenException,
    RefreshTokenExpiredException,
    PasswordResetTokenExpiredException,
    InvalidPasswordResetTokenException,
    EncryptionException,
    DatabaseException
)
from app.services.email_service import EmailService
import traceback
import secrets

logger = get_logger(__name__)


class AuthService:

    @staticmethod
    async def authenticate_user(email: str, senha: str, db: AsyncSession) -> dict:
        try:
            user = await UserRepository.find_by_email(email, db)

            if not user:
                logger.warning("login_failed", email=email, reason="user_not_found")
                raise InvalidCredentialsException()

            if not verify_password(senha, user.senha):
                logger.warning("login_failed", email=email, reason="invalid_password")
                raise InvalidCredentialsException()

            user.last_login = datetime.now(timezone.utc)

            token_data = {"user_id": user.id, "email": user.email}
            access_token = create_access_token(token_data)
            refresh_token = create_refresh_token(token_data)

            refresh_token_expires = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
            user.refresh_token = refresh_token
            user.refresh_token_expires = refresh_token_expires

            await UserRepository.update(user, db)

            try:
                user_response = UserResponse(
                    id=user.id,
                    nome=user.nome,
                    sobrenome=user.sobrenome,
                    cpf=user.cpf,
                    email=user.email,
                    cep=user.cep,
                    logradouro=user.logradouro,
                    numero=user.numero,
                    complemento=user.complemento,
                    bairro=user.bairro,
                    cidade=user.cidade,
                    estado=user.estado
                )
            except Exception as e:
                logger.error("user_response_error", email=email, error=str(e), traceback=traceback.format_exc())
                raise EncryptionException(
                    message="Erro ao processar dados criptografados do usuário",
                    operation="decrypt"
                )

            logger.info("login_success", user_id=user.id, email=email)

            return {
                "user": user_response,
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }

        except (InvalidCredentialsException, EncryptionException):
            raise
        except Exception as e:
            logger.error("authentication_error", error=str(e), traceback=traceback.format_exc())
            raise DatabaseException(
                message="Erro ao processar autenticação",
                operation="authenticate",
                original_error=str(e)
            )

    @staticmethod
    async def refresh_access_token(refresh_token: str, db: AsyncSession) -> dict:
        try:
            payload = verify_refresh_token(refresh_token)
            user_id = payload.get("user_id")

            user = await UserRepository.find_by_id(user_id, db)
            if not user:
                logger.warning("refresh_failed", user_id=user_id, reason="user_not_found")
                raise UserNotFoundException(user_id=user_id)

            if user.refresh_token != refresh_token:
                logger.warning("refresh_failed", user_id=user_id, reason="invalid_token")
                raise InvalidTokenException(message="Refresh token inválido")

            if user.refresh_token_expires < datetime.now(timezone.utc):
                logger.warning("refresh_failed", user_id=user_id, reason="token_expired")
                raise RefreshTokenExpiredException()

            token_data = {"user_id": user.id, "email": user.email}
            new_access_token = create_access_token(token_data)

            logger.info("token_refreshed", user_id=user_id)

            return {
                "access_token": new_access_token,
                "token_type": "bearer"
            }

        except (UserNotFoundException, InvalidTokenException, RefreshTokenExpiredException):
            raise
        except Exception as e:
            logger.error("refresh_token_error", error=str(e))
            raise DatabaseException(
                message="Erro ao renovar token",
                operation="refresh_token",
                original_error=str(e)
            )

    @staticmethod
    async def logout(user_id: int, db: AsyncSession) -> dict:
        try:
            user = await UserRepository.find_by_id(user_id, db)
            if not user:
                raise UserNotFoundException(user_id=user_id)

            user.refresh_token = None
            user.refresh_token_expires = None
            await UserRepository.update(user, db)

            logger.info("logout_success", user_id=user_id)

            return {"detail": "Logout realizado com sucesso."}

        except UserNotFoundException:
            raise
        except Exception as e:
            logger.error("logout_error", user_id=user_id, error=str(e))
            raise DatabaseException(
                message="Erro ao fazer logout",
                operation="logout",
                original_error=str(e)
            )

    @staticmethod
    async def request_password_reset(email: str, db: AsyncSession) -> dict:
        try:
            user = await UserRepository.find_by_email(email, db)

            success_message = "Se o e-mail estiver cadastrado, você receberá instruções para resetar sua senha."

            if not user:
                logger.warning("password_reset_requested", email=email, reason="user_not_found")
                return {"detail": success_message}

            reset_token = secrets.token_urlsafe(32)

            expiration_hours = settings.password_reset_expire_hours
            user.password_reset_token = reset_token
            user.password_reset_expires = datetime.now(timezone.utc) + timedelta(hours=expiration_hours)

            await UserRepository.update(user, db)

            logger.info("password_reset_token_generated", user_id=user.id, email=email)

            email_sent = await EmailService.send_password_reset_email(
                to_email=user.email,
                user_name=user.nome,
                reset_token=reset_token,
                expiration_hours=expiration_hours
            )

            if email_sent:
                logger.info("password_reset_email_sent", user_id=user.id, email=email)
            else:
                logger.error("password_reset_email_failed", user_id=user.id, email=email)

            return {"detail": success_message}

        except Exception as e:
            logger.error("password_reset_request_error", error=str(e), traceback=traceback.format_exc())
            raise DatabaseException(
                message="Erro ao processar solicitação de reset de senha",
                operation="request_password_reset",
                original_error=str(e)
            )

    @staticmethod
    async def reset_password(token: str, new_password: str, db: AsyncSession) -> dict:
        try:
            from sqlalchemy import select
            from app.models.user_model import UserModel

            result = await db.execute(
                select(UserModel).where(UserModel.password_reset_token == token)
            )
            user = result.scalar_one_or_none()

            if not user:
                logger.warning("password_reset_failed", reason="invalid_token")
                raise InvalidPasswordResetTokenException()

            if user.password_reset_expires < datetime.now(timezone.utc):
                logger.warning("password_reset_failed", user_id=user.id, reason="token_expired")
                raise PasswordResetTokenExpiredException()

            user.senha = hash_password(new_password)
            user.password_reset_token = None
            user.password_reset_expires = None

            user.refresh_token = None
            user.refresh_token_expires = None

            await UserRepository.update(user, db)

            logger.info("password_reset_success", user_id=user.id)

            change_date = datetime.now(timezone.utc).strftime("%d/%m/%Y às %H:%M")
            email_sent = await EmailService.send_password_changed_email(
                to_email=user.email,
                user_name=user.nome,
                change_date=change_date
            )

            if email_sent:
                logger.info("password_changed_email_sent", user_id=user.id)
            else:
                logger.error("password_changed_email_failed", user_id=user.id)

            return {
                "detail": "Senha resetada com sucesso. Faça login com sua nova senha."
            }

        except (InvalidPasswordResetTokenException, PasswordResetTokenExpiredException):
            raise
        except Exception as e:
            logger.error("password_reset_error", error=str(e), traceback=traceback.format_exc())
            raise DatabaseException(
                message="Erro ao resetar senha",
                operation="reset_password",
                original_error=str(e)
            )
