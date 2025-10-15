from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_model import UserModel
from app.core.security import encrypt_data, decrypt_data
from typing import List, Optional
import structlog

logger = structlog.get_logger(__name__)


class UserRepository:

    @staticmethod
    def _decrypt_user(user: UserModel) -> Optional[UserModel]:
        if not user:
            return user

        try:
            user.cpf = decrypt_data(user.cpf)
            user.cep = decrypt_data(user.cep)
            user.logradouro = decrypt_data(user.logradouro)
            user.numero = decrypt_data(user.numero)
            if user.complemento:
                user.complemento = decrypt_data(user.complemento)
            user.bairro = decrypt_data(user.bairro)
            user.cidade = decrypt_data(user.cidade)
            user.estado = decrypt_data(user.estado)
            return user
        except ValueError as e:
            logger.error(
                "user_decryption_failed",
                user_id=user.id,
                email=user.email,
                error=str(e)
            )
            return None

    @staticmethod
    def _encrypt_user_data(user: UserModel) -> None:
        if user.cpf and not user.cpf.startswith('gAAAAA'):
            user.cpf = encrypt_data(user.cpf)
        if user.cep and not user.cep.startswith('gAAAAA'):
            user.cep = encrypt_data(user.cep)
        if user.logradouro and not user.logradouro.startswith('gAAAAA'):
            user.logradouro = encrypt_data(user.logradouro)
        if user.numero and not user.numero.startswith('gAAAAA'):
            user.numero = encrypt_data(user.numero)
        if user.complemento and not user.complemento.startswith('gAAAAA'):
            user.complemento = encrypt_data(user.complemento)
        if user.bairro and not user.bairro.startswith('gAAAAA'):
            user.bairro = encrypt_data(user.bairro)
        if user.cidade and not user.cidade.startswith('gAAAAA'):
            user.cidade = encrypt_data(user.cidade)
        if user.estado and not user.estado.startswith('gAAAAA'):
            user.estado = encrypt_data(user.estado)

    @staticmethod
    async def find_by_id(user_id: int, db: AsyncSession) -> Optional[UserModel]:
        result = await db.execute(select(UserModel).where(UserModel.id == user_id))
        user = result.scalar_one_or_none()
        return UserRepository._decrypt_user(user)

    @staticmethod
    async def find_by_email(email: str, db: AsyncSession) -> Optional[UserModel]:
        result = await db.execute(select(UserModel).where(UserModel.email == email))
        user = result.scalar_one_or_none()
        return UserRepository._decrypt_user(user)

    @staticmethod
    async def find_by_cpf(cpf: str, db: AsyncSession) -> Optional[UserModel]:
        """
        TODO: Implementar hash determinístico para otimizar performance.
        """
        result = await db.execute(select(UserModel))
        all_users = result.scalars().all()

        for user in all_users:
            decrypted_user = UserRepository._decrypt_user(user)
            if decrypted_user and decrypted_user.cpf == cpf:
                return decrypted_user

        return None

    @staticmethod
    async def find_by_nome(nome: str, db: AsyncSession) -> List[UserModel]:
        result = await db.execute(select(UserModel).where(UserModel.nome == nome))
        users = result.scalars().all()
        return [UserRepository._decrypt_user(user) for user in users]

    @staticmethod
    async def find_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[UserModel]:
        result = await db.execute(
            select(UserModel)
            .offset(skip)
            .limit(limit)
        )
        users = result.scalars().all()
        return [UserRepository._decrypt_user(user) for user in users]

    @staticmethod
    async def create(
        nome: str,
        sobrenome: str,
        cpf: str,
        email: str,
        senha_hash: str,
        db: AsyncSession,
        cep: str,
        logradouro: str,
        numero: str,
        bairro: str,
        cidade: str,
        estado: str,
        complemento: Optional[str] = None
    ) -> UserModel:
        db_user = UserModel(
            nome=nome,
            sobrenome=sobrenome,
            cpf=encrypt_data(cpf),
            email=email,
            senha=senha_hash,
            cep=encrypt_data(cep),
            logradouro=encrypt_data(logradouro),
            numero=encrypt_data(numero),
            complemento=encrypt_data(complemento) if complemento else None,
            bairro=encrypt_data(bairro),
            cidade=encrypt_data(cidade),
            estado=encrypt_data(estado)
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return UserRepository._decrypt_user(db_user)

    @staticmethod
    async def update(user: UserModel, db: AsyncSession) -> UserModel:
        UserRepository._encrypt_user_data(user)
        await db.commit()
        await db.refresh(user)
        return UserRepository._decrypt_user(user)

    @staticmethod
    async def delete(user: UserModel, db: AsyncSession) -> None:
        await db.delete(user)
        await db.commit()
