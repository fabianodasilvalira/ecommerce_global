import enum
from sqlalchemy import Column, Integer, String, DECIMAL, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class MetodoPagamentoEnum(enum.Enum):
    PIX = "PIX"
    CARTAO_CREDITO = "CARTAO_CREDITO"
    CARTAO_DEBITO = "CARTAO_DEBITO"
    BOLETO = "BOLETO"
    CARTEIRA_DIGITAL = "CARTEIRA_DIGITAL"  # tipo PicPay, MercadoPago, PayPal


class StatusPagamento(enum.Enum):
    PENDENTE = "PENDENTE"          # Pedido gerado, aguardando pagamento
    EM_ANALISE = "EM_ANALISE"       # Pagamento recebido, mas em análise (ex.: antifraude)
    APROVADO = "APROVADO"           # Pagamento confirmado
    RECUSADO = "RECUSADO"           # Pagamento recusado pela operadora
    CANCELADO = "CANCELADO"         # Pedido cancelado manualmente ou por timeout
    ESTORNADO = "ESTORNADO"         # Pagamento devolvido após cancelamento ou disputa



class Pagamento(Base):
    __tablename__ = "pagamento"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("venda.id", ondelete="CASCADE"), nullable=False)

    valor = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(StatusPagamento), nullable=False)

    metodo_pagamento = Column(Enum(MetodoPagamentoEnum), nullable=False)
    transacao_id = Column(String(100), nullable=True)             # ID retornado pelo gateway

    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    venda = relationship("Venda", back_populates="pagamentos")
    historicos = relationship("HistoricoPagamento", back_populates="pagamento", cascade="all, delete-orphan")
