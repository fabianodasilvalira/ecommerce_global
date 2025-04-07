import enum
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class StatusHistoricoPagamento(enum.Enum):
    PENDENTE = "PENDENTE"
    AUTORIZADO = "AUTORIZADO"
    FALHOU = "FALHOU"
    CANCELADO = "CANCELADO"
    ESTORNADO = "ESTORNADO"


class HistoricoPagamento(Base):
    __tablename__ = "historico_pagamento"

    id = Column(Integer, primary_key=True, index=True)
    pagamento_id = Column(Integer, ForeignKey("pagamento.id", ondelete="CASCADE"), nullable=False)

    status = Column(Enum(StatusHistoricoPagamento), nullable=False)
    metodo_pagamento = Column(String(50), nullable=True)  # opcional: cartão, pix, boleto
    observacao = Column(String(255), nullable=True)       # opcional: "falha na verificação de cartão"
    data_evento = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    pagamento = relationship("Pagamento", back_populates="historicos")
