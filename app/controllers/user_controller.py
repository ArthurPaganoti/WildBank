from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user_schema import User, UserResponse, UserResponsePublic, UserResponseLimited
from app.services.user_service import UserService
from app.services.auth_service import AuthService


class UserController:

    @staticmethod
    async def register_user(user_data: User, db: AsyncSession) -> UserResponse:
        return await UserService.create_user(user_data, db)

    @staticmethod
    async def login(email: str, senha: str, db: AsyncSession) -> dict:
        return await AuthService.authenticate_user(email, senha, db)

    @staticmethod
    async def refresh_token(refresh_token: str, db: AsyncSession) -> dict:
        return await AuthService.refresh_access_token(refresh_token, db)

    @staticmethod
    async def logout(user_id: int, db: AsyncSession) -> dict:
        return await AuthService.logout(user_id, db)

    @staticmethod
    async def get_all_users_public(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[UserResponsePublic]:
        return await UserService.get_all_users_public(db, skip=skip, limit=limit)

    @staticmethod
    async def get_user_by_id(user_id: int, db: AsyncSession) -> UserResponse:
        return await UserService.get_user_by_id(user_id, db)

    @staticmethod
    async def get_user_by_email_public(email: str, db: AsyncSession) -> UserResponsePublic:
        return await UserService.get_user_by_email_public(email, db)

    @staticmethod
    async def get_users_by_nome_limited(nome: str, db: AsyncSession) -> List[UserResponseLimited]:
        return await UserService.get_users_by_nome_limited(nome, db)

    @staticmethod
    async def update_user(user_id: int, new_email: str, new_password: str, db: AsyncSession, current_user_id: int) -> UserResponse:
        return await UserService.update_user(user_id, new_email, new_password, db, current_user_id)

    @staticmethod
    async def delete_user(user_id: int, db: AsyncSession, current_user_id: int) -> dict:
        return await UserService.delete_user(user_id, db, current_user_id)

    @staticmethod
    async def request_password_reset(email: str, db: AsyncSession) -> dict:
        return await AuthService.request_password_reset(email, db)

    @staticmethod
    async def reset_password(token: str, new_password: str, db: AsyncSession) -> dict:
        return await AuthService.reset_password(token, new_password, db)
