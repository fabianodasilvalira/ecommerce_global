from sqlalchemy import Column, Integer, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum  # Import necessário

# Enum para status da entrega
class StatusEntregaEnum(str, enum.Enum):
    PENDENTE = "pendente"
    A_CAMINHO = "a caminho"
    ENTREGUE = "entregue"

# Modelo de Entrega
class Entrega(Base):
    __tablename__ = "entrega"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("venda.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(StatusEntregaEnum), nullable=False, default=StatusEntregaEnum.PENDENTE)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    venda = relationship("Venda", back_populates="entrega")
    entregador_id = Column(Integer, ForeignKey("usuario.id", ondelete="SET NULL"), nullable=True)

    entregador = relationship("Usuario", foreign_keys=[entregador_id])
    candidatos = relationship("EntregaCandidato", back_populates="entrega", cascade="all, delete-orphan")

