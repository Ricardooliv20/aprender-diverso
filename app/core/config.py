from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações da aplicação, carregadas do arquivo .env"""

    APP_NAME: str = "Aprender Diverso"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # Banco de dados
    DATABASE_URL: str = "sqlite:///./aprender_diverso.db"

    # Segurança / JWT
    SECRET_KEY: str = "troque-esta-chave"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Retorna as configurações (com cache para não reler o .env toda vez)"""
    return Settings()