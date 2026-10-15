from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import exigir_perfil, obter_usuario_atual
from app.models.usuario import Usuario
from app.schemas.relatorio import RelatorioCreate, RelatorioResponse
from app.services import relatorio_service

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.post("/gerar", response_model=RelatorioResponse, status_code=status.HTTP_201_CREATED)
def gerar_relatorio(
    dados: RelatorioCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("professor", "admin")),
):
    """Gera um relatório bimestral a partir dos micro-feedbacks acumulados."""
    try:
        return relatorio_service.gerar_relatorio(
            db=db,
            aluno_id=dados.aluno_id,
            periodo=dados.periodo,
            gerado_por_id=usuario.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/aluno/{aluno_id}", response_model=List[RelatorioResponse])
def listar_relatorios_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    """Lista todos os relatórios de um aluno (mais recentes primeiro)."""
    return relatorio_service.listar_por_aluno(db, aluno_id)


@router.get("/{relatorio_id}", response_model=RelatorioResponse)
def obter_relatorio(
    relatorio_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    relatorio = relatorio_service.obter_por_id(db, relatorio_id)
    if not relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    return relatorio