from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey, DECIMAL, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum

# Enum para status da venda
class StatusVendaEnum(str, enum.Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    CANCELADO = "cancelado"

# Modelo de Venda
class Venda(Base):
    __tablename__ = "venda"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    endereco_id = Column(Integer, ForeignKey("endereco.id"), nullable=True)
    cupom_id = Column(Integer, ForeignKey("cupom.id"), nullable=True)
    total = Column(Float, nullable=False, default=0.0)
    status = Column(Enum(StatusVendaEnum), nullable=False, default=StatusVendaEnum.PENDENTE)
    data_venda = Column(TIMESTAMP, server_default=func.now())

    usuario = relationship("Usuario", back_populates="vendas")
    endereco = relationship("Endereco", back_populates="vendas")
    cupom = relationship("Cupom", back_populates="vendas")
    entrega = relationship("Entrega", back_populates="venda", uselist=False)
