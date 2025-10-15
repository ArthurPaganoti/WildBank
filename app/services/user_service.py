from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import User, UserResponse, UserResponsePublic, UserResponseLimited
from app.core.security import hash_password
from app.core.logging import get_logger
from app.core.cache import get_cache, set_cache, delete_cache
from app.exceptions import (
    EmailAlreadyExistsException,
    CPFAlreadyExistsException,
    UserNotFoundException,
    UnauthorizedAccountAccessException,
    CacheException
)

logger = get_logger(__name__)


class UserService:

    @staticmethod
    async def create_user(user_data: User, db: AsyncSession) -> UserResponse:
        existing_user = await UserRepository.find_by_email(user_data.email, db)
        if existing_user:
            logger.warning("user_creation_failed", email=user_data.email, reason="email_exists")
            raise EmailAlreadyExistsException(email=user_data.email)

        existing_cpf = await UserRepository.find_by_cpf(user_data.cpf, db)
        if existing_cpf:
            logger.warning("user_creation_failed", cpf=user_data.cpf[:3] + "***", reason="cpf_exists")
            raise CPFAlreadyExistsException(cpf=user_data.cpf)

        senha_hash = hash_password(user_data.senha)

        db_user = await UserRepository.create(
            nome=user_data.nome,
            sobrenome=user_data.sobrenome,
            cpf=user_data.cpf,
            email=user_data.email,
            senha_hash=senha_hash,
            db=db,
            cep=user_data.cep,
            logradouro=user_data.logradouro,
            numero=user_data.numero,
            complemento=user_data.complemento,
            bairro=user_data.bairro,
            cidade=user_data.cidade,
            estado=user_data.estado
        )

        logger.info("user_created", user_id=db_user.id, email=db_user.email)

        return UserResponse(
            id=db_user.id,
            nome=db_user.nome,
            sobrenome=db_user.sobrenome,
            cpf=db_user.cpf,
            email=db_user.email,
            cep=db_user.cep,
            logradouro=db_user.logradouro,
            numero=db_user.numero,
            complemento=db_user.complemento,
            bairro=db_user.bairro,
            cidade=db_user.cidade,
            estado=db_user.estado
        )

    @staticmethod
    async def get_all_users_public(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[UserResponsePublic]:
        users = await UserRepository.find_all(db, skip=skip, limit=limit)
        logger.info("users_public_listed", count=len(users), skip=skip, limit=limit)
        return [
            UserResponsePublic(
                id=user.id,
                nome=user.nome,
                sobrenome=user.sobrenome,
                email=user.email
            ) for user in users
        ]

    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession) -> UserResponse:
        cache_key = f"user:{user_id}"

        try:
            cached_user = await get_cache(cache_key)
            if cached_user:
                logger.info("user_retrieved_from_cache", user_id=user_id)
                return cached_user
        except Exception as e:
            logger.warning("cache_get_failed", user_id=user_id, error=str(e))

        user = await UserRepository.find_by_id(user_id, db)
        if not user:
            logger.warning("user_not_found", user_id=user_id)
            raise UserNotFoundException(user_id=user_id)

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

        try:
            await set_cache(cache_key, user_response, expire=300)
        except Exception as e:
            logger.warning("cache_set_failed", user_id=user_id, error=str(e))

        logger.info("user_retrieved", user_id=user_id)
        return user_response

    @staticmethod
    async def get_user_by_email_public(email: str, db: AsyncSession) -> UserResponsePublic:
        user = await UserRepository.find_by_email(email, db)
        if not user:
            logger.warning("user_not_found", email=email)
            raise UserNotFoundException(email=email)
        return UserResponsePublic(
            id=user.id,
            nome=user.nome,
            sobrenome=user.sobrenome,
            email=user.email
        )

    @staticmethod
    async def get_users_by_nome_limited(nome: str, db: AsyncSession) -> List[UserResponseLimited]:
        users = await UserRepository.find_by_nome(nome, db)
        return [
            UserResponseLimited(
                id=user.id,
                nome=user.nome,
                sobrenome=user.sobrenome
            ) for user in users
        ]

    @staticmethod
    async def update_user(user_id: int, new_email: str, new_password: str, db: AsyncSession,
                          current_user_id: int) -> UserResponse:
        if current_user_id != user_id:
            logger.warning("unauthorized_update_attempt", user_id=user_id, current_user_id=current_user_id)
            raise UnauthorizedAccountAccessException(action="atualizar")

        existing_user = await UserRepository.find_by_email(new_email, db)
        if existing_user and existing_user.id != user_id:
            logger.warning("email_conflict", email=new_email, user_id=user_id)
            raise EmailAlreadyExistsException(email=new_email)

        user = await UserRepository.find_by_id(user_id, db)
        if not user:
            logger.warning("user_not_found", user_id=user_id)
            raise UserNotFoundException(user_id=user_id)

        user.email = new_email
        user.senha = hash_password(new_password)
        updated_user = await UserRepository.update(user, db)
        logger.info("user_updated", user_id=user_id)

        cache_key = f"user:{user_id}"
        try:
            await set_cache(cache_key, updated_user, expire=300)
        except Exception as e:
            logger.warning("cache_set_failed", user_id=user_id, error=str(e))

        return UserResponse(
            id=updated_user.id,
            nome=updated_user.nome,
            sobrenome=updated_user.sobrenome,
            cpf=updated_user.cpf,
            email=updated_user.email,
            cep=updated_user.cep,
            logradouro=updated_user.logradouro,
            numero=updated_user.numero,
            complemento=updated_user.complemento,
            bairro=updated_user.bairro,
            cidade=updated_user.cidade,
            estado=updated_user.estado
        )

    @staticmethod
    async def delete_user(user_id: int, db: AsyncSession, current_user_id: int) -> dict:
        if current_user_id != user_id:
            logger.warning("unauthorized_delete_attempt", user_id=user_id, current_user_id=current_user_id)
            raise UnauthorizedAccountAccessException(action="deletar")

        user = await UserRepository.find_by_id(user_id, db)
        if not user:
            logger.warning("user_not_found", user_id=user_id)
            raise UserNotFoundException(user_id=user_id)

        await UserRepository.delete(user, db)
        logger.info("user_deleted", user_id=user_id)

        cache_key = f"user:{user_id}"
        try:
            await delete_cache(cache_key)
        except Exception as e:
            logger.warning("cache_delete_failed", user_id=user_id, error=str(e))

        return {"detail": "Usuário deletado com sucesso."}
