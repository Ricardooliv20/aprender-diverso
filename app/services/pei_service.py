from typing import Optional

from sqlalchemy.orm import Session

from app.models.aluno import Aluno
from app.models.pei import PEI, AdaptacaoPEI, ObjetivoPEI
from app.schemas.pei import (
    AdaptacaoPEICreate,
    ObjetivoPEICreate,
    PEICreate,
    PEIUpdate,
)


def obter_por_aluno(db: Session, aluno_id: int) -> Optional[PEI]:
    return db.query(PEI).filter(PEI.aluno_id == aluno_id).first()


def criar(db: Session, dados: PEICreate) -> PEI:
    if not db.query(Aluno).filter(Aluno.id == dados.aluno_id).first():
        raise ValueError("Aluno não encontrado")

    if obter_por_aluno(db, dados.aluno_id):
        raise ValueError("Este aluno já possui um PEI cadastrado")

    pei = PEI(**dados.model_dump())
    db.add(pei)
    db.commit()
    db.refresh(pei)
    return pei


def atualizar(db: Session, pei: PEI, dados: PEIUpdate) -> PEI:
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(pei, campo, valor)
    db.commit()
    db.refresh(pei)
    return pei


def adicionar_objetivo(db: Session, pei_id: int, dados: ObjetivoPEICreate) -> ObjetivoPEI:
    obj = ObjetivoPEI(pei_id=pei_id, **dados.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def adicionar_adaptacao(db: Session, pei_id: int, dados: AdaptacaoPEICreate) -> AdaptacaoPEI:
    adp = AdaptacaoPEI(pei_id=pei_id, **dados.model_dump())
    db.add(adp)
    db.commit()
    db.refresh(adp)
    return adp


def deletar_objetivo(db: Session, objetivo_id: int) -> None:
    obj = db.query(ObjetivoPEI).filter(ObjetivoPEI.id == objetivo_id).first()
    if obj:
        db.delete(obj)
        db.commit()


def deletar_adaptacao(db: Session, adaptacao_id: int) -> None:
    adp = db.query(AdaptacaoPEI).filter(AdaptacaoPEI.id == adaptacao_id).first()
    if adp:
        db.delete(adp)
        db.commit()