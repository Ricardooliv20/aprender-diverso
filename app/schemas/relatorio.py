from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RelatorioCreate(BaseModel):
    aluno_id: int
    periodo: str  # ex: "1º Bimestre 2026"


class RelatorioResponse(BaseModel):
    id: int
    aluno_id: int
    gerado_por_id: int
    periodo: str
    conteudo: str
    criado_em: datetime

    class Config:
        from_attributes = True