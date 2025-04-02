import enum
from sqlalchemy import Column, Integer, Float, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Enum para status do pagamento
class StatusPagamento(enum.Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    CANCELADO = "CANCELADO"

# Modelo de Pagamento
class Pagamento(Base):
    __tablename__ = "pagamento"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("venda.id"), nullable=False)
    valor = Column(Float, nullable=False)
    status = Column(Enum(StatusPagamento), nullable=False)  # Corrigido para ENUM
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)  # Novo
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)  # Novo

    venda = relationship("Venda")
