from pydantic import Extra
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
    API_HOST: str
    API_PORT: int
    API_RELOAD: bool
    API_WORKERS: int

    # Permite variáveis extras no arquivo .env (como ADMIN_EMAIL, ADMIN_PASSWORD)
    class Config:
        env_file = ".env"
        extra = Extra.allow  # Permite que variáveis extras sejam carregadas

settings = Settings()
