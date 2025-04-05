
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Endereco(Base):
    __tablename__ = "endereco"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(10), nullable=False)
    complemento = Column(String(100))
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(9), nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    ativo = Column(Boolean, default=True)


    # Relacionamentos corrigidos
    usuario = relationship("Usuario", back_populates="enderecos")
    vendas = relationship("Venda", back_populates="endereco")