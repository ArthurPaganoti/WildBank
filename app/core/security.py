from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from cryptography.fernet import Fernet, InvalidToken
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import structlog

logger = structlog.get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()


def _get_cipher():
    encryption_key = os.getenv("ENCRYPTION_KEY")
    if not encryption_key:
        raise ValueError(
            "ENCRYPTION_KEY não está definida! "
            "Execute: openssl rand -hex 32 "
            "e adicione ENCRYPTION_KEY ao arquivo .env"
        )

    encryption_salt = os.getenv("ENCRYPTION_SALT")
    if not encryption_salt:
        raise ValueError(
            "ENCRYPTION_SALT não está definida! "
            "Execute: openssl rand -hex 16 "
            "e adicione ENCRYPTION_SALT ao arquivo .env"
        )

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=encryption_salt.encode(),
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(encryption_key.encode()))
    return Fernet(key)


try:
    cipher = _get_cipher()
except ValueError as e:
    print(f"ERRO DE CONFIGURAÇÃO: {e}")
    cipher = None


def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        password = password_bytes.decode('utf-8', errors='ignore')

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        plain_password = password_bytes.decode('utf-8', errors='ignore')

    return pwd_context.verify(plain_password, hashed_password)


def encrypt_data(data: str) -> str:
    if not data:
        return data
    if cipher is None:
        raise ValueError("Cipher não inicializado. Verifique ENCRYPTION_KEY e ENCRYPTION_SALT no .env")
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()


def decrypt_data(encrypted_data: str) -> str:
    if not encrypted_data:
        return encrypted_data
    if cipher is None:
        raise ValueError("Cipher não inicializado. Verifique ENCRYPTION_KEY e ENCRYPTION_SALT no .env")

    try:
        decrypted = cipher.decrypt(encrypted_data.encode())
        return decrypted.decode()
    except InvalidToken:
        logger.error(
            "decryption_failed",
            error="InvalidToken",
            message="Dados criptografados com chave diferente ou corrompidos"
        )
        raise ValueError(
            "Falha na descriptografia: dados foram criptografados com chave diferente. "
            "Verifique ENCRYPTION_KEY e ENCRYPTION_SALT no .env ou re-crie os dados."
        )
    except Exception as e:
        logger.error("decryption_error", error=str(e))
        raise


def hash_sensitive_data(data: str, salt: str = None) -> str:
    import hashlib
    if not salt:
        salt = os.getenv("HASH_SALT", "default_salt_change_me")
    combined = f"{data}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido.")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")


def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("user_id")
        token_type: str = payload.get("type")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido.")

        if token_type != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido. Use um refresh token.")

        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado.")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Token não fornecido.")
    return verify_token(credentials.credentials)