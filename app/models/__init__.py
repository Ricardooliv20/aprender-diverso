from app.models.usuario import Usuario
from app.models.turma import Turma
from app.models.aluno import Aluno
from app.models.professor_turma import ProfessorTurma
from app.models.responsavel_aluno import ResponsavelAluno
from app.models.pei import PEI, ObjetivoPEI, AdaptacaoPEI
from app.models.feedback import Feedback
from app.models.tcle import TCLE
from app.models.relatorio import Relatorio

__all__ = [
    "Usuario",
    "Turma",
    "Aluno",
    "ProfessorTurma",
    "ResponsavelAluno",
    "PEI",
    "ObjetivoPEI",
    "AdaptacaoPEI",
    "Feedback",
    "TCLE",
    "Relatorio",
]