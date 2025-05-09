from pydantic import Extra, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = False
    API_WORKERS: int = 1

    # Variáveis específicas para admin, podem ter defaults ou serem obrigatórias
    ADMIN_EMAIL: str = Field(default="admin@example.com")
    ADMIN_PASSWORD: str = Field(default="adminpass")

    class Config:
        env_file = ".env"
        extra = Extra.ignore  # Mudar para ignore para evitar carregar variáveis não definidas no schema
        # Ou manter allow se houver outras variáveis de ambiente que você deseja carregar e não estão no schema

settings = Settings()

