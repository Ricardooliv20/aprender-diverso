from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import exigir_perfil, obter_usuario_atual
from app.models.usuario import Usuario
from app.schemas.pei import (
    AdaptacaoPEICreate,
    AdaptacaoPEIResponse,
    ObjetivoPEICreate,
    ObjetivoPEIResponse,
    PEICreate,
    PEIResponse,
    PEIUpdate,
)
from app.services import pei_service

router = APIRouter(prefix="/peis", tags=["PEI"])


@router.get("/aluno/{aluno_id}", response_model=PEIResponse)
def obter_pei_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(obter_usuario_atual),
):
    pei = pei_service.obter_por_aluno(db, aluno_id)
    if not pei:
        raise HTTPException(status_code=404, detail="PEI não encontrado para este aluno")
    return pei


@router.post("/", response_model=PEIResponse, status_code=status.HTTP_201_CREATED)
def criar_pei(
    dados: PEICreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("professor", "admin")),
):
    try:
        return pei_service.criar(db, dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{pei_id}", response_model=PEIResponse)
def atualizar_pei(
    pei_id: int,
    dados: PEIUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("professor", "admin")),
):
    from app.models.pei import PEI
    pei = db.query(PEI).filter(PEI.id == pei_id).first()
    if not pei:
        raise HTTPException(status_code=404, detail="PEI não encontrado")
    return pei_service.atualizar(db, pei, dados)


@router.post("/{pei_id}/objetivos", response_model=ObjetivoPEIResponse, status_code=201)
def adicionar_objetivo(
    pei_id: int,
    dados: ObjetivoPEICreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("professor", "admin")),
):
    return pei_service.adicionar_objetivo(db, pei_id, dados)


@router.post("/{pei_id}/adaptacoes", response_model=AdaptacaoPEIResponse, status_code=201)
def adicionar_adaptacao(
    pei_id: int,
    dados: AdaptacaoPEICreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("professor", "admin")),
):
    return pei_service.adicionar_adaptacao(db, pei_id, dados)


@router.delete("/objetivos/{objetivo_id}", status_code=204)
def deletar_objetivo(
    objetivo_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("professor", "admin")),
):
    pei_service.deletar_objetivo(db, objetivo_id)


@router.delete("/adaptacoes/{adaptacao_id}", status_code=204)
def deletar_adaptacao(
    adaptacao_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(exigir_perfil("professor", "admin")),
):
    pei_service.deletar_adaptacao(db, adaptacao_id)