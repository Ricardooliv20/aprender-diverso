from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class ResponsavelAluno(Base):
    __tablename__ = "responsavel_aluno"

    id = Column(Integer, primary_key=True, index=True)
    responsavel_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    parentesco = Column(String(50), nullable=True)

    responsavel = relationship("Usuario", back_populates="alunos_como_responsavel")
    aluno = relationship("Aluno", back_populates="responsaveis")