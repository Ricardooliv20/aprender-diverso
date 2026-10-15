from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PEI(Base):
    __tablename__ = "peis"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), unique=True, nullable=False)
    resumo = Column(Text, nullable=True)
    ativo = Column(String(20), default="ativo")
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    aluno = relationship("Aluno", back_populates="pei")
    objetivos = relationship(
        "ObjetivoPEI", back_populates="pei", cascade="all, delete-orphan"
    )
    adaptacoes = relationship(
        "AdaptacaoPEI", back_populates="pei", cascade="all, delete-orphan"
    )


class ObjetivoPEI(Base):
    __tablename__ = "objetivos_pei"

    id = Column(Integer, primary_key=True, index=True)
    pei_id = Column(Integer, ForeignKey("peis.id"), nullable=False)
    descricao = Column(Text, nullable=False)
    status = Column(String(30), default="em_andamento")

    pei = relationship("PEI", back_populates="objetivos")


class AdaptacaoPEI(Base):
    __tablename__ = "adaptacoes_pei"

    id = Column(Integer, primary_key=True, index=True)
    pei_id = Column(Integer, ForeignKey("peis.id"), nullable=False)
    descricao = Column(Text, nullable=False)

    pei = relationship("PEI", back_populates="adaptacoes")