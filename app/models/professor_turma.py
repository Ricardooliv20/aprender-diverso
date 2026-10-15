from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class ProfessorTurma(Base):
    __tablename__ = "professor_turma"

    id = Column(Integer, primary_key=True, index=True)
    professor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)

    professor = relationship("Usuario", back_populates="turmas_como_professor")
    turma = relationship("Turma", back_populates="professores")