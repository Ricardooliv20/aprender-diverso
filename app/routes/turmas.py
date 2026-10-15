from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import exigir_perfil, obter_usuario_atual
from app.models.usuario import Usuario
from app.schemas.turma import TurmaCreate, TurmaResponse, TurmaUpdate
from app.services import turma_service

router = APIRouter(prefix="/turmas", tags=["Turmas"])


@router.get("/", response_model=List[TurmaResponse])
def listar_turmas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    """Lista todas as turmas (qualquer usuário autenticado)."""
    return turma_service.listar(db)


@router.get("/{turma_id}", response_model=TurmaResponse)
def obter_turma(
    turma_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    turma = turma_service.obter_por_id(db, turma_id)
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return turma


@router.post("/", response_model=TurmaResponse, status_code=status.HTTP_201_CREATED)
def criar_turma(
    dados: TurmaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("admin")),
):
    """Somente administradores podem criar turmas."""
    return turma_service.criar(db, dados)


@router.put("/{turma_id}", response_model=TurmaResponse)
def atualizar_turma(
    turma_id: int,
    dados: TurmaUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("admin")),
):
    turma = turma_service.obter_por_id(db, turma_id)
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return turma_service.atualizar(db, turma, dados)


@router.delete("/{turma_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_turma(
    turma_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("admin")),
):
    turma = turma_service.obter_por_id(db, turma_id)
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    turma_service.deletar(db, turma)