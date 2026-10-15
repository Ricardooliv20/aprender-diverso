from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import exigir_perfil, obter_usuario_atual
from app.models.usuario import Usuario
from app.schemas.aluno import AlunoCreate, AlunoResponse, AlunoUpdate
from app.services import aluno_service

router = APIRouter(prefix="/alunos", tags=["Alunos"])


@router.get("/", response_model=List[AlunoResponse])
def listar_alunos(
    turma_id: Optional[int] = None,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    """Lista alunos. Pode filtrar por turma usando ?turma_id=1"""
    return aluno_service.listar(db, turma_id)


@router.get("/{aluno_id}", response_model=AlunoResponse)
def obter_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    aluno = aluno_service.obter_por_id(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


@router.post("/", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def criar_aluno(
    dados: AlunoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("admin")),
):
    """Somente admin pode cadastrar alunos."""
    try:
        return aluno_service.criar(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(
    aluno_id: int,
    dados: AlunoUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("admin")),
):
    aluno = aluno_service.obter_por_id(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    try:
        return aluno_service.atualizar(db, aluno, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("admin")),
):
    aluno = aluno_service.obter_por_id(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    aluno_service.deletar(db, aluno)