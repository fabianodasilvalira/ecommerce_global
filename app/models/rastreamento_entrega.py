from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Modelo de Rastreamento de Entrega
class RastreamentoEntrega(Base):
    __tablename__ = "rastreamento_entrega"

    id = Column(Integer, primary_key=True, index=True)
    entrega_id = Column(Integer, ForeignKey("entrega.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(100), nullable=False)
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)  # Atualiza sempre

    entrega = relationship("Entrega", cascade="all, delete")
