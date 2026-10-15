from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    ano_letivo = Column(Integer, nullable=False)
    turno = Column(String(20), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    professores = relationship(
        "ProfessorTurma", back_populates="turma", cascade="all, delete-orphan"
    )
    alunos = relationship(
        "Aluno", back_populates="turma", cascade="all, delete-orphan"
    )