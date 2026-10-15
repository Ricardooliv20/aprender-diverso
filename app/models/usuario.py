from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    perfil = Column(String(20), nullable=False)  # "admin", "professor", "responsavel"
    telefone = Column(String(20), nullable=True)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    turmas_como_professor = relationship(
        "ProfessorTurma", back_populates="professor", cascade="all, delete-orphan"
    )
    alunos_como_responsavel = relationship(
        "ResponsavelAluno", back_populates="responsavel", cascade="all, delete-orphan"
    )
    feedbacks_criados = relationship(
        "Feedback", back_populates="professor", cascade="all, delete-orphan"
    )