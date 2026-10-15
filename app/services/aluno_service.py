from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.aluno import Aluno
from app.models.turma import Turma
from app.schemas.aluno import AlunoCreate, AlunoUpdate


def listar(db: Session, turma_id: Optional[int] = None) -> List[Aluno]:
    query = db.query(Aluno)
    if turma_id:
        query = query.filter(Aluno.turma_id == turma_id)
    return query.order_by(Aluno.nome).all()


def obter_por_id(db: Session, aluno_id: int) -> Optional[Aluno]:
    return db.query(Aluno).filter(Aluno.id == aluno_id).first()


def criar(db: Session, dados: AlunoCreate) -> Aluno:
    # valida se turma existe
    if not db.query(Turma).filter(Turma.id == dados.turma_id).first():
        raise ValueError("Turma não encontrada")

    aluno = Aluno(**dados.model_dump())
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno


def atualizar(db: Session, aluno: Aluno, dados: AlunoUpdate) -> Aluno:
    valores = dados.model_dump(exclude_unset=True)

    # se está trocando de turma, valida
    if "turma_id" in valores:
        if not db.query(Turma).filter(Turma.id == valores["turma_id"]).first():
            raise ValueError("Turma não encontrada")

    for campo, valor in valores.items():
        setattr(aluno, campo, valor)
    db.commit()
    db.refresh(aluno)
    return aluno


def deletar(db: Session, aluno: Aluno) -> None:
    db.delete(aluno)
    db.commit()