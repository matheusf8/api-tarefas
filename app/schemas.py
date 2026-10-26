from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class TaskCreate(BaseModel):
    titulo: str
    descricao: str | None = None


class TaskUpdate(BaseModel):
    titulo: str
    descricao: str | None = None
    concluida: bool


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descricao: str | None = None
    concluida: bool
    criada_em: datetime


class UserCreate(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=8)

    @field_validator("senha")
    @classmethod
    def senha_ate_72_bytes(cls, v: str) -> str:
        # o bcrypt só aceita até 72 bytes (letras com acento ocupam 2)
        if len(v.encode("utf-8")) > 72:
            raise ValueError("A senha pode ter no máximo 72 bytes")
        return v


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    criado_em: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
