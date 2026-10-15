from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

# Contexto para hash de senhas (bcrypt é o padrão mais seguro)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- SENHAS ----------

def gerar_hash_senha(senha: str) -> str:
    """Transforma a senha em hash (nunca salvar senha pura!)"""
    return pwd_context.hash(senha)


def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    """Compara a senha digitada com o hash salvo no banco"""
    return pwd_context.verify(senha_pura, senha_hash)


# ---------- JWT ----------

def criar_token_acesso(dados: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT com os dados do usuário.
    Exemplo de uso: criar_token_acesso({"sub": "email@x.com", "perfil": "professor"})
    """
    dados_copia = dados.copy()
    expira = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    dados_copia.update({"exp": expira})

    token = jwt.encode(dados_copia, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def decodificar_token(token: str) -> Optional[dict]:
    """Decodifica e valida o token. Retorna os dados ou None se inválido."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None