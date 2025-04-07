from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, Boolean
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
    senha = Column(String(255), nullable=False)
    cpf_cnpj = Column(String(20), unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    tipo_usuario = Column(Enum(TipoUsuarioEnum), nullable=False)
    refresh_token = Column(String(500), nullable=True)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)  # <- novo campo

    # Relacionamentos corrigidos
    enderecos = relationship("Endereco", back_populates="usuario", cascade="all, delete-orphan")
    vendas = relationship("Venda", back_populates="usuario", cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="usuario", cascade="all, delete-orphan")  # Adicionado
    lista_desejos = relationship("ListaDesejos", back_populates="usuario", cascade="all, delete-orphan")
