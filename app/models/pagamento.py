import enum
from sqlalchemy import Column, Integer, DECIMAL, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class StatusPagamento(enum.Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    CANCELADO = "CANCELADO"

class Pagamento(Base):
    __tablename__ = "pagamento"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("venda.id", ondelete="CASCADE"), nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(StatusPagamento), nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    venda = relationship("Venda", back_populates="pagamentos")
