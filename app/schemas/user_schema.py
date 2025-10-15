from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re
from app.utils.cpf_validator import validar_cpf, formatar_cpf

ESTADOS_VALIDOS = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

class User(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, description="Nome do usuário")
    sobrenome: str = Field(..., min_length=2, max_length=100, description="Sobrenome do usuário")
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF do usuário")
    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(..., min_length=8, max_length=48, description="Senha do usuário")

    cep: str = Field(..., max_length=9, description="CEP")
    logradouro: str = Field(..., min_length=3, max_length=255, description="Rua/Avenida")
    numero: str = Field(..., min_length=1, max_length=20, description="Número")
    complemento: Optional[str] = Field(None, max_length=100, description="Complemento")
    bairro: str = Field(..., min_length=2, max_length=100, description="Bairro")
    cidade: str = Field(..., min_length=2, max_length=100, description="Cidade")
    estado: str = Field(..., min_length=2, max_length=2, description="Estado (UF)")

    @field_validator('nome', 'sobrenome')
    @classmethod
    def validate_nome(cls, v: str) -> str:
        v = v.strip()

        if len(v) < 2:
            raise ValueError('Nome/Sobrenome deve ter no mínimo 2 caracteres')
        if len(v) > 100:
            raise ValueError('Nome/Sobrenome deve ter no máximo 100 caracteres')

        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', v):
            raise ValueError('Nome/Sobrenome deve conter apenas letras')

        return v

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        if not validar_cpf(v):
            raise ValueError('CPF inválido. Verifique os dígitos e tente novamente.')
        return formatar_cpf(v)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: EmailStr) -> str:
        return str(v).lower().strip()

    @field_validator('senha')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        if len(v) > 48:
            raise ValueError('Senha deve ter no máximo 48 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra maiúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra minúscula')
        if not re.search(r'\d', v):
            raise ValueError('Senha deve conter pelo menos um número')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;`~]', v):
            raise ValueError('Senha deve conter pelo menos um caractere especial')
        return v

    @field_validator('cep')
    @classmethod
    def validate_cep(cls, v: str) -> str:
        cep_clean = re.sub(r'\D', '', v)
        if len(cep_clean) != 8:
            raise ValueError('CEP deve ter 8 dígitos')
        return v

    @field_validator('logradouro')
    @classmethod
    def validate_logradouro(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError('Logradouro deve ter no mínimo 3 caracteres')
        if len(v) > 255:
            raise ValueError('Logradouro deve ter no máximo 255 caracteres')
        return v

    @field_validator('bairro', 'cidade')
    @classmethod
    def validate_address_field(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError('Campo deve ter no mínimo 2 caracteres')
        if len(v) > 100:
            raise ValueError('Campo deve ter no máximo 100 caracteres')
        return v

    @field_validator('numero')
    @classmethod
    def validate_numero(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 1:
            raise ValueError('Número é obrigatório')
        if v.upper() not in ['S/N', 'SN'] and not re.search(r'\d', v):
            raise ValueError('Número deve conter pelo menos um dígito ou ser "S/N"')
        return v

    @field_validator('complemento')
    @classmethod
    def validate_complemento(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == '':
            return None
        v = v.strip()
        if len(v) > 100:
            raise ValueError('Complemento deve ter no máximo 100 caracteres')
        return v

    @field_validator('estado')
    @classmethod
    def validate_estado(cls, v: str) -> str:
        v = v.upper().strip()
        if len(v) != 2:
            raise ValueError('Estado deve ter 2 caracteres (UF)')
        if v not in ESTADOS_VALIDOS:
            raise ValueError(f'Estado inválido. Use uma UF válida: {", ".join(ESTADOS_VALIDOS)}')
        return v

class UserResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    cpf: str
    email: EmailStr
    cep: str
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: str

    class Config:
        from_attributes = True

class UserResponsePublic(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserResponseLimited(BaseModel):
    id: int
    nome: str
    sobrenome: str

    class Config:
        from_attributes = True


class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., description="E-mail do usuário para reset de senha")


class PasswordResetConfirm(BaseModel):
    token: str = Field(..., min_length=20, description="Token de reset de senha")
    new_password: str = Field(..., min_length=8, max_length=48, description="Nova senha")

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        if len(v) > 48:
            raise ValueError('Senha deve ter no máximo 48 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra maiúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra minúscula')
        if not re.search(r'\d', v):
            raise ValueError('Senha deve conter pelo menos um número')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;`~]', v):
            raise ValueError('Senha deve conter pelo menos um caractere especial')
        return v
