from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ---------- Schema base (atributos comuns) ----------
class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    perfil: str = Field(..., pattern="^(admin|professor|responsavel)$")
    telefone: Optional[str] = None


# ---------- Schema para criação (recebe do frontend) ----------
class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6, max_length=100)


# ---------- Schema para login ----------
class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


# ---------- Schema para resposta (o que o frontend recebe) ----------
class UsuarioResponse(UsuarioBase):
    id: int
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True  # permite ler de objetos SQLAlchemy


# ---------- Schema do token JWT ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse