from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field, field_validator


class FeedbackBase(BaseModel):
    aluno_id: int
    categorias: Dict[str, str] = Field(
        ...,
        description="Tags categorizadas. Chaves: foco, sensorial, social, tarefas",
    )
    observacao: Optional[str] = Field(None, max_length=280)

    @field_validator("categorias")
    @classmethod
    def validar_categorias(cls, v):
        valores_validos = {
            "foco": {"otimo", "bom", "regular", "dificuldade"},
            "sensorial": {"calmo", "agitado", "sobrecarga", "retraido"},
            "social": {"participativo", "colaborativo", "isolado", "conflito"},
            "tarefas": {"concluiu", "parcial", "nao-concluiu", "recusou"},
        }

        for chave, valor in v.items():
            if chave not in valores_validos:
                raise ValueError(f"Categoria inválida: {chave}")
            if valor not in valores_validos[chave]:
                raise ValueError(
                    f"Valor '{valor}' inválido para categoria '{chave}'"
                )

        if len(v) == 0:
            raise ValueError("Pelo menos uma categoria deve ser informada")

        return v


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackResponse(FeedbackBase):
    id: int
    professor_id: int
    criado_em: datetime

    class Config:
        from_attributes = True