import enum
from sqlalchemy import Column, Integer, Float, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Enum para tipo de movimentação
class TipoMovimentoEnum(enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

# Modelo de Movimentação de Estoque
class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacao_estoque"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("venda.id"), nullable=True)  # ou False, se for obrigatório
    produto_id = Column(Integer, ForeignKey("produto.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    tipo_movimentacao = Column(Enum(TipoMovimentoEnum), nullable=False)  # Usando o Enum TipoMovimentacao
    data = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)  # Novo
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)  # Novo

    produto = relationship("Produto")

    venda = relationship("Venda")


