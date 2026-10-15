from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import exigir_perfil, obter_usuario_atual
from app.models.usuario import Usuario
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.services import feedback_service

router = APIRouter(prefix="/feedbacks", tags=["Feedbacks"])


@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def criar_feedback(
    dados: FeedbackCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("professor", "admin")),
):
    """Registra um micro-feedback (somente professor ou admin)."""
    try:
        return feedback_service.criar(db, dados, professor_id=usuario.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/aluno/{aluno_id}", response_model=List[FeedbackResponse])
def listar_feedbacks_aluno(
    aluno_id: int,
    limite: int = 50,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    """Lista feedbacks de um aluno (mais recentes primeiro)."""
    return feedback_service.listar_por_aluno(db, aluno_id, limite)


@router.get("/aluno/{aluno_id}/estatisticas")
def estatisticas_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
) -> Dict:
    """
    Retorna estatísticas do aluno para o dashboard:
    - total de feedbacks
    - percentuais por categoria
    - dados agrupados por semana (para o gráfico)
    """
    feedbacks = feedback_service.listar_por_aluno(db, aluno_id, limite=1000)

    return {
        "aluno_id": aluno_id,
        "total_feedbacks": len(feedbacks),
        "percentuais": feedback_service.calcular_percentuais(feedbacks),
        "grafico": feedback_service.agrupar_por_semana(feedbacks),
    }


@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("professor", "admin")),
):
    feedback = feedback_service.obter_por_id(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback não encontrado")
    feedback_service.deletar(db, feedback)