from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ---------- Objetivos ----------
class ObjetivoPEIBase(BaseModel):
    descricao: str = Field(..., min_length=5)
    status: str = Field("em_andamento", pattern="^(em_andamento|concluido)$")


class ObjetivoPEICreate(ObjetivoPEIBase):
    pass


class ObjetivoPEIResponse(ObjetivoPEIBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Adaptações ----------
class AdaptacaoPEIBase(BaseModel):
    descricao: str = Field(..., min_length=5)


class AdaptacaoPEICreate(AdaptacaoPEIBase):
    pass


class AdaptacaoPEIResponse(AdaptacaoPEIBase):
    id: int

    class Config:
        from_attributes = True


# ---------- PEI ----------
class PEIBase(BaseModel):
    aluno_id: int
    resumo: Optional[str] = None


class PEICreate(PEIBase):
    pass


class PEIUpdate(BaseModel):
    resumo: Optional[str] = None
    ativo: Optional[str] = None


class PEIResponse(PEIBase):
    id: int
    ativo: str
    criado_em: datetime
    objetivos: List[ObjetivoPEIResponse] = []
    adaptacoes: List[AdaptacaoPEIResponse] = []

    class Config:
        from_attributes = True