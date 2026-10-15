from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Relatorio(Base):
    __tablename__ = "relatorios"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    gerado_por_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    periodo = Column(String(50), nullable=False)          # ex: "1º Bimestre 2026"
    conteudo = Column(Text, nullable=False)               # o texto gerado
    percentuais = Column(Text, nullable=True)             # JSON com percentuais (salvo como texto)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    aluno = relationship("Aluno")
    gerado_por = relationship("Usuario")