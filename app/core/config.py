from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DATABASE_URL: str  # Adicionado para garantir que a URL seja carregada corretamente
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    API_HOST: str
    API_PORT: int
    API_RELOAD: bool
    API_WORKERS: int

    class Config:
        env_file = ".env"

settings = Settings()
