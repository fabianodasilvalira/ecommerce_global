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

    total = Column(DECIMAL(10, 2), nullable=False, default=0.00)  # Valor total final
    valor_total_bruto = Column(DECIMAL(10, 2), nullable=False, default=0.00)  # Total sem desconto
    valor_desconto = Column(DECIMAL(10, 2), nullable=False, default=0.00)  # Valor do desconto aplicado

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
        post_update=True
    )

    # Método para calcular e aplicar os descontos na venda
    def aplicar_descontos(self):
        # Calcular o total bruto da venda (somando os itens)
        self.valor_total_bruto = sum(item.valor_total for item in self.carrinho.itens)

        # Aplicar cupom de desconto, se houver
        if self.cupom:
            self.tipo_desconto = TipoDescontoEnum.CUPOM
            self.valor_desconto += self.cupom.calcular_desconto(self.valor_total_bruto)

        # Aplicar promoção, se houver
        if self.promocao:
            self.tipo_desconto = TipoDescontoEnum.PROMOCAO
            self.valor_desconto += self.promocao.calcular_desconto(self.valor_total_bruto)

        # Atualizar o total com o desconto aplicado
        self.total = self.valor_total_bruto - self.valor_desconto
