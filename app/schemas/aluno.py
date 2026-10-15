from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class AlunoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    data_nascimento: date
    diagnostico: Optional[str] = None
    observacoes: Optional[str] = None
    turma_id: int


class AlunoCreate(AlunoBase):
    pass


class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    data_nascimento: Optional[date] = None
    diagnostico: Optional[str] = None
    observacoes: Optional[str] = None
    turma_id: Optional[int] = None


class AlunoResponse(AlunoBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True