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
    PENDENTE = "PENDENTE"
    EM_ANALISE = "EM_ANALISE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"
    CANCELADO = "CANCELADO"
    ESTORNADO = "ESTORNADO"

class Pagamento(Base):
    __tablename__ = "pagamento"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("venda.id", ondelete="CASCADE"), nullable=False)

    valor = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(StatusPagamento), nullable=False)
    metodo_pagamento = Column(Enum(MetodoPagamentoEnum), nullable=False)

    # Informações comuns
    transacao_id = Column(String(100), nullable=True)  # ID retornado pelo gateway
    numero_parcelas = Column(Integer, nullable=True)   # Ex: 6 parcelas
    bandeira_cartao = Column(String(50), nullable=True) # Ex: VISA, MasterCard
    ultimos_digitos_cartao = Column(String(4), nullable=True) # Apenas 4 últimos dígitos
    nome_cartao = Column(String(100), nullable=True)    # Nome do titular (opcional)

    # Campos específicos para PIX
    codigo_pix = Column(String(300), nullable=True)     # Código de pagamento do PIX

    # Campos específicos para boleto
    linha_digitavel_boleto = Column(String(300), nullable=True) # Linha digitável do boleto

    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    venda = relationship("Venda", back_populates="pagamentos")
    historicos = relationship("HistoricoPagamento", back_populates="pagamento", cascade="all, delete-orphan")
