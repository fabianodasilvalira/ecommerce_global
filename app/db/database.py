# app/db/database.py
import os

from fastapi import Depends
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()  # Isso vai carregar o conteúdo do arquivo .env

# Usando as variáveis carregadas no .env
DATABASE_URL = os.getenv('DATABASE_URL')

# Criando o engine e a sessão com SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função para obter a sessão do banco de dados
def get_db(db: Session = Depends(SessionLocal)):
    try:
        yield db
    finally:
        db.close()
