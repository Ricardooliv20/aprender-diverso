from typing import Optional
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.core.security import gerar_hash_senha, verificar_senha


def obter_por_email(db: Session, email: str) -> Optional[Usuario]:
    """Busca um usuário pelo e-mail"""
    return db.query(Usuario).filter(Usuario.email == email).first()


def obter_por_id(db: Session, usuario_id: int) -> Optional[Usuario]:
    """Busca um usuário pelo ID"""
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def criar_usuario(db: Session, dados: UsuarioCreate) -> Usuario:
    """Cria um novo usuário com a senha criptografada"""
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        perfil=dados.perfil,
        telefone=dados.telefone,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def autenticar(db: Session, email: str, senha: str) -> Optional[Usuario]:
    """Verifica e-mail e senha. Retorna o usuário se estiver correto."""
    usuario = obter_por_email(db, email)
    if not usuario:
        return None
    if not verificar_senha(senha, usuario.senha_hash):
        return None
    return usuario