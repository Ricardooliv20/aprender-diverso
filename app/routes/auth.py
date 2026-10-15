from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import obter_usuario_atual
from app.core.security import criar_token_acesso
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, Token
from app.services import usuario_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/registrar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar(dados: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário no sistema."""
    # Verifica se e-mail já existe
    if usuario_service.obter_por_email(db, dados.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado no sistema",
        )

    usuario = usuario_service.criar_usuario(db, dados)
    return usuario


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Login via e-mail e senha (formato OAuth2).
    Observação: o campo 'username' do OAuth2 deve ser preenchido com o e-mail.
    """
    usuario = usuario_service.autenticar(db, form_data.username, form_data.password)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = criar_token_acesso({
        "sub": usuario.email,
        "perfil": usuario.perfil,
        "nome": usuario.nome,
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": usuario,
    }


@router.get("/me", response_model=UsuarioResponse)
def obter_meu_perfil(usuario: Usuario = Depends(obter_usuario_atual)):
    """Retorna os dados do usuário logado (rota protegida)."""
    return usuario