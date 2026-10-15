from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()

# Cria o engine de conexão
# Para SQLite, precisa do parâmetro check_same_thread=False
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG  # mostra o SQL no terminal em modo debug
)

# Fábrica de sessões do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos (tabelas)
Base = declarative_base()


def get_db():
    """
    Dependência do FastAPI: abre uma sessão do banco e fecha ao final da requisição.
    Uso nas rotas: def minha_rota(db: Session = Depends(get_db))
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()