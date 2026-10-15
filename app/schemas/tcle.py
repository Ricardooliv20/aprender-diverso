from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TCLEBase(BaseModel):
    aluno_id: int
    responsavel_id: int


class TCLECreate(TCLEBase):
    pass


class TCLEAceite(BaseModel):
    aceito: bool


class TCLEResponse(TCLEBase):
    id: int
    aceito: bool
    aceito_em: Optional[datetime] = None
    criado_em: datetime

    class Config:
        from_attributes = True