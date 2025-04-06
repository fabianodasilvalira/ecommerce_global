# Adicione no início do arquivo:
from sqlalchemy import Column, Integer, Enum, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class StatusVendaEnum(str, enum.Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    CANCELADO = "cancelado"

class Venda(Base):
    __tablename__ = "venda"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    endereco_id = Column(Integer, ForeignKey("endereco.id", ondelete="SET NULL"), nullable=True)
    cupom_id = Column(Integer, ForeignKey("cupom.id", ondelete="SET NULL"), nullable=True)
    total = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    status = Column(Enum(StatusVendaEnum, name="status_venda_enum"), nullable=False, default=StatusVendaEnum.PENDENTE)
    data_venda = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # Relacionamentos atualizados (usando string references)
    usuario = relationship("Usuario", back_populates="vendas")
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")  # Corrigido para 'itens'
    endereco = relationship("Endereco", back_populates="vendas")
    cupom = relationship("Cupom", back_populates="vendas")
    entrega = relationship("Entrega", back_populates="venda", uselist=False)