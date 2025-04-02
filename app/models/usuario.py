from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class TipoUsuarioEnum(str, enum.Enum):
    CLIENTE = "cliente"
    ADMIN = "admin"
    FUNCIONARIO = "funcionario"
    ENTREGADOR = "entregador"

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha = Column(String(60), nullable=False)  # Compatível com bcrypt
    cpf_cnpj = Column(String(20), unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    tipo_usuario = Column(Enum(TipoUsuarioEnum), nullable=False)
    refresh_token = Column(String(500), nullable=True)  # Novo campo para armazenar o refresh token
    criado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # Atualiza quando editado
