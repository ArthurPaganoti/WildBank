from fastapi import APIRouter, Depends, Request
from typing import List
from app.schemas.user_schema import (
    User, UserResponse, UserResponsePublic, UserResponseLimited,
    PasswordResetRequest, PasswordResetConfirm
)
from app.controllers.user_controller import UserController
from app.core.database import get_db
from app.core.security import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr, Field
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.exceptions import ValidationException
import re

router = APIRouter(prefix="/users", tags=["users"])

limiter = Limiter(key_func=get_remote_address)

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(..., min_length=8, max_length=48, description="Senha do usuário")

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Refresh token para renovação")

class UpdateUserRequest(BaseModel):
    email: EmailStr = Field(..., description="Novo e-mail do usuário")
    senha: str = Field(..., min_length=8, max_length=48, description="Nova senha do usuário")

@router.post("/login", response_model=None)
@limiter.limit("5/minute")
async def login(request: Request, login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await UserController.login(login_data.email, login_data.senha, db)

@router.post("/refresh", response_model=None)
async def refresh_token(refresh_data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    return await UserController.refresh_token(refresh_data.refresh_token, db)

@router.post("/logout", response_model=None)
async def logout(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserController.logout(current_user['user_id'], db)

@router.post("/", status_code=201, response_model=UserResponse)
async def register_user(user: User, db: AsyncSession = Depends(get_db)):
    return await UserController.register_user(user, db)

@router.get("/", response_model=List[UserResponsePublic])
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    if limit > 100:
        raise ValidationException(
            message="Limite máximo é 100 registros por página",
            field="limit",
            details={"max": 100, "provided": limit}
        )
    if skip < 0:
        raise ValidationException(
            message="Skip não pode ser negativo",
            field="skip",
            details={"provided": skip}
        )
    return await UserController.get_all_users_public(db, skip=skip, limit=limit)

@router.get("/me", response_model=UserResponse)
async def get_current_user_data(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserController.get_user_by_id(current_user['user_id'], db)

@router.get("/get/nome/{nome}", response_model=List[UserResponseLimited])
async def get_users_by_nome(
    nome: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome):
        raise ValidationException(
            message="Nome deve conter apenas letras",
            field="nome",
            details={"provided": nome}
        )
    if len(nome) < 2:
        raise ValidationException(
            message="Nome deve ter pelo menos 2 caracteres",
            field="nome",
            details={"min_length": 2, "provided_length": len(nome)}
        )
    return await UserController.get_users_by_nome_limited(nome, db)

@router.get("/get/email/{email}", response_model=UserResponsePublic)
async def get_user_by_email_route(
    email: EmailStr,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserController.get_user_by_email_public(email, db)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserController.delete_user(user_id, db, current_user['user_id'])

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_route(
    user_id: int,
    update_data: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await UserController.update_user(user_id, update_data.email, update_data.senha, db, current_user['user_id'])

@router.post("/password-reset/request", response_model=None)
@limiter.limit("3/hour")
async def request_password_reset(
    request: Request,
    reset_request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    return await UserController.request_password_reset(reset_request.email, db)

@router.post("/password-reset/confirm", response_model=None)
async def confirm_password_reset(
    reset_confirm: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    return await UserController.reset_password(reset_confirm.token, reset_confirm.new_password, db)
