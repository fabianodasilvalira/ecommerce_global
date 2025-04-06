from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class StatusEntregaCandidato(str, enum.Enum):
    pendente = 'pendente'
    aceita = 'aceita'
    recusada = 'recusada'


class EntregaCandidato(Base):
    __tablename__ = "entrega_candidato"

    id = Column(Integer, primary_key=True, index=True)
    entrega_id = Column(Integer, ForeignKey("entrega.id", ondelete="CASCADE"), nullable=False)
    entregador_id = Column(Integer, ForeignKey("entregador.id", ondelete="CASCADE"), nullable=False)
    data_interesse = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(StatusEntregaCandidato), default=StatusEntregaCandidato.pendente, nullable=False)

    # Relacionamentos
    entrega = relationship("Entrega", back_populates="candidatos")
    entregador = relationship("Entregador", back_populates="entregas_candidatadas")

    def __repr__(self):
        return f"<EntregaCandidato(entregador={self.entregador_id}, entrega={self.entrega_id}, status={self.status})>"
