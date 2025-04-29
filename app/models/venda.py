from sqlalchemy import Column, Integer, Enum as SqlEnum, TIMESTAMP, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum

# Enums Python
class StatusVendaEnum(str, enum.Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    CANCELADO = "cancelado"

class TipoDescontoEnum(str, enum.Enum):
    NENHUM = "nenhum"
    CUPOM = "cupom"
    PROMOCAO = "promocao"

class StatusPagamentoEnum(str, enum.Enum):
    PENDENTE = "pendente"
    EM_ANALISE = "em_analise"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    CANCELADO = "cancelado"
    ESTORNADO = "estornado"

class Venda(Base):
    __tablename__ = "venda"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    endereco_id = Column(Integer, ForeignKey("endereco.id", ondelete="SET NULL"), nullable=True)
    cupom_id = Column(Integer, ForeignKey("cupom.id", ondelete="SET NULL"), nullable=True)
    carrinho_id = Column(Integer, ForeignKey("carrinho.id", ondelete="SET NULL"), nullable=True)

    total = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    valor_total_bruto = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    valor_desconto = Column(DECIMAL(10, 2), nullable=False, default=0.00)

    tipo_desconto = Column(
        SqlEnum(TipoDescontoEnum, name="tipodescontoenum", native_enum=True, create_constraint=True),
        nullable=False,
        default=TipoDescontoEnum.NENHUM
    )

    status = Column(
        SqlEnum(StatusVendaEnum, name="status_venda_enum", native_enum=True, create_constraint=True),
        nullable=False,
        default=StatusVendaEnum.PENDENTE
    )

    status_pagamento = Column(
        SqlEnum(StatusPagamentoEnum, name="status_pagamento_enum", native_enum=True, create_constraint=True),
        nullable=False,
        default=StatusPagamentoEnum.PENDENTE
    )

    data_venda = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    is_ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="vendas")
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")
    endereco = relationship("Endereco", back_populates="vendas")
    cupom = relationship("Cupom", back_populates="vendas")
    entrega = relationship("Entrega", back_populates="venda", uselist=False)
    pagamentos = relationship("Pagamento", back_populates="venda")
    carrinho = relationship(
        "Carrinho",
        back_populates="venda",
        uselist=False,
        post_update=True  # Importante para relações one-to-one bidirecionais
    )

    # Lógica de atualização do status da venda com base no status dos pagamentos
    def atualizar_status_venda(self):
        if all(pagamento.status == StatusPagamentoEnum.APROVADO for pagamento in self.pagamentos):
            self.status = StatusVendaEnum.PAGO
        elif any(pagamento.status == StatusPagamentoEnum.CANCELADO for pagamento in self.pagamentos):
            self.status = StatusVendaEnum.CANCELADO
        else:
            self.status = StatusVendaEnum.PENDENTE
