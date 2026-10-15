from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import exigir_perfil, obter_usuario_atual
from app.models.usuario import Usuario
from app.schemas.tcle import TCLECreate, TCLEResponse
from app.services import tcle_service

router = APIRouter(prefix="/tcles", tags=["TCLE"])


@router.get("/aluno/{aluno_id}", response_model=TCLEResponse)
def obter_tcle_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    tcle = tcle_service.obter_por_aluno(db, aluno_id)
    if not tcle:
        raise HTTPException(status_code=404, detail="TCLE não encontrado para este aluno")
    return tcle


@router.post("/", response_model=TCLEResponse, status_code=status.HTTP_201_CREATED)
def criar_tcle(
    dados: TCLECreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("admin")),
):
    try:
        return tcle_service.criar(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/aluno/{aluno_id}/aceitar", response_model=TCLEResponse)
def aceitar_tcle(
    aluno_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    """Registra o aceite do TCLE (responsável ou admin)."""
    if usuario.perfil not in ("responsavel", "admin"):
        raise HTTPException(status_code=403, detail="Apenas responsável ou admin pode aceitar")

    tcle = tcle_service.obter_por_aluno(db, aluno_id)
    if not tcle:
        raise HTTPException(status_code=404, detail="TCLE não encontrado")

    return tcle_service.aceitar(db, tcle)