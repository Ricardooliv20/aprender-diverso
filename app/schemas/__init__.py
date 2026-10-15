from app.schemas.usuario import (
    UsuarioBase, UsuarioCreate, UsuarioLogin, UsuarioResponse, Token,
)
from app.schemas.turma import TurmaBase, TurmaCreate, TurmaUpdate, TurmaResponse
from app.schemas.aluno import AlunoBase, AlunoCreate, AlunoUpdate, AlunoResponse
from app.schemas.feedback import FeedbackBase, FeedbackCreate, FeedbackResponse
from app.schemas.tcle import TCLEBase, TCLECreate, TCLEAceite, TCLEResponse
from app.schemas.relatorio import RelatorioCreate, RelatorioResponse

__all__ = [
    "UsuarioBase", "UsuarioCreate", "UsuarioLogin", "UsuarioResponse", "Token",
    "TurmaBase", "TurmaCreate", "TurmaUpdate", "TurmaResponse",
    "AlunoBase", "AlunoCreate", "AlunoUpdate", "AlunoResponse",
    "FeedbackBase", "FeedbackCreate", "FeedbackResponse",
    "PEIBase", "PEICreate", "PEIUpdate", "PEIResponse",
    "ObjetivoPEIBase", "ObjetivoPEICreate", "ObjetivoPEIResponse",
    "AdaptacaoPEIBase", "AdaptacaoPEICreate", "AdaptacaoPEIResponse",
    "TCLEBase", "TCLECreate", "TCLEAceite", "TCLEResponse",
        # Relatório
    "RelatorioCreate", "RelatorioResponse",
]

from app.schemas.pei import (
    PEIBase, PEICreate, PEIUpdate, PEIResponse,
    ObjetivoPEIBase, ObjetivoPEICreate, ObjetivoPEIResponse,
    AdaptacaoPEIBase, AdaptacaoPEICreate, AdaptacaoPEIResponse,
)
