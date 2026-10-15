from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.aluno import Aluno
from app.models.tcle import TCLE
from app.models.usuario import Usuario
from app.schemas.tcle import TCLECreate


def obter_por_aluno(db: Session, aluno_id: int) -> Optional[TCLE]:
    return db.query(TCLE).filter(TCLE.aluno_id == aluno_id).first()


def criar(db: Session, dados: TCLECreate) -> TCLE:
    if not db.query(Aluno).filter(Aluno.id == dados.aluno_id).first():
        raise ValueError("Aluno não encontrado")
    if not db.query(Usuario).filter(Usuario.id == dados.responsavel_id).first():
        raise ValueError("Responsável não encontrado")

    if obter_por_aluno(db, dados.aluno_id):
        raise ValueError("Este aluno já possui um TCLE cadastrado")

    tcle = TCLE(**dados.model_dump())
    db.add(tcle)
    db.commit()
    db.refresh(tcle)
    return tcle


def aceitar(db: Session, tcle: TCLE) -> TCLE:
    tcle.aceito = True
    tcle.aceito_em = datetime.utcnow()
    db.commit()
    db.refresh(tcle)
    return tcle