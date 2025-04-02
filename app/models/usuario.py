from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
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
    senha = Column(String(255), nullable=False)  # Alterado para 255 para compatibilidade com hashing forte
    cpf_cnpj = Column(String(20), unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    tipo_usuario = Column(Enum(TipoUsuarioEnum), nullable=False)
    refresh_token = Column(String(500), nullable=True)  # Mantido para armazenar refresh tokens
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamentos (se necessário)
    vendas = relationship("Venda", back_populates="usuario", cascade="all, delete-orphan")

