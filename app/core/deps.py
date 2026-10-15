from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decodificar_token
from app.models.usuario import Usuario
from app.services import usuario_service

# URL usada pelo Swagger para o botão "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    """Verifica o token JWT e retorna o usuário logado."""
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decodificar_token(token)
    if payload is None:
        raise credenciais_invalidas

    email: str = payload.get("sub")
    if email is None:
        raise credenciais_invalidas

    usuario = usuario_service.obter_por_email(db, email)
    if usuario is None or not usuario.ativo:
        raise credenciais_invalidas

    return usuario


def exigir_perfil(*perfis_permitidos: str):
    """
    Retorna uma dependência que só permite acesso aos perfis informados.
    Uso: Depends(exigir_perfil("admin", "professor"))
    """
    def verificador(usuario: Usuario = Depends(obter_usuario_atual)) -> Usuario:
        if usuario.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este recurso",
            )
        return usuario
    return verificador