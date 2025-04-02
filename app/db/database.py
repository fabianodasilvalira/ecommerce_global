import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Usando a variável DATABASE_URL do .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Criando o engine e a sessão com SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()  # Cria uma nova sessão
    try:
        yield db
    finally:
        db.close()
