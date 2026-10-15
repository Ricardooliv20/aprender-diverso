from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TurmaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=50)
    ano_letivo: int = Field(..., ge=2020, le=2100)
    turno: str = Field(..., pattern="^(manha|tarde|noite|integral)$")


class TurmaCreate(TurmaBase):
    pass


class TurmaUpdate(BaseModel):
    nome: Optional[str] = None
    ano_letivo: Optional[int] = None
    turno: Optional[str] = None


class TurmaResponse(TurmaBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True