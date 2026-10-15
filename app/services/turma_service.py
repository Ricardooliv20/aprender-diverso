from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.turma import Turma
from app.schemas.turma import TurmaCreate, TurmaUpdate


def listar(db: Session) -> List[Turma]:
    return db.query(Turma).order_by(Turma.nome).all()


def obter_por_id(db: Session, turma_id: int) -> Optional[Turma]:
    return db.query(Turma).filter(Turma.id == turma_id).first()


def criar(db: Session, dados: TurmaCreate) -> Turma:
    turma = Turma(**dados.model_dump())
    db.add(turma)
    db.commit()
    db.refresh(turma)
    return turma


def atualizar(db: Session, turma: Turma, dados: TurmaUpdate) -> Turma:
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(turma, campo, valor)
    db.commit()
    db.refresh(turma)
    return turma


def deletar(db: Session, turma: Turma) -> None:
    db.delete(turma)
    db.commit()