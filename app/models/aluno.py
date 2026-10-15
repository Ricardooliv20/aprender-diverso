from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    diagnostico = Column(String(200), nullable=True)
    observacoes = Column(Text, nullable=True)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    turma = relationship("Turma", back_populates="alunos")
    responsaveis = relationship(
        "ResponsavelAluno", back_populates="aluno", cascade="all, delete-orphan"
    )
    pei = relationship(
        "PEI", back_populates="aluno", uselist=False, cascade="all, delete-orphan"
    )
    feedbacks = relationship(
        "Feedback", back_populates="aluno", cascade="all, delete-orphan"
    )
    tcle = relationship(
        "TCLE", back_populates="aluno", uselist=False, cascade="all, delete-orphan"
    )