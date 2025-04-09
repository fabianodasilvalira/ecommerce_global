from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float, Boolean
from sqlalchemy.orm import relationship
from decimal import Decimal
from datetime import datetime
from app.db.database import Base

class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=True)
    preco = Column(DECIMAL(10, 2), nullable=False)
    volume = Column(Float, nullable=True)
    unidade_medida = Column(String(10), nullable=True)
    ativo = Column(Boolean, default=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="SET NULL"), nullable=True)
    margem_lucro = Column(DECIMAL(5, 2), nullable=False, default=20.00)
    preco_final = Column(DECIMAL(10, 2), nullable=False)

    imagens = relationship("ProdutoImagem", back_populates="produto", lazy="joined", cascade="all, delete-orphan")
    estoque = relationship("Estoque", back_populates="produto", uselist=False, cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="produto", cascade="all, delete-orphan")
    promocoes = relationship("Promocao", back_populates="produto", cascade="all, delete-orphan")
    categoria = relationship("Categoria", back_populates="produtos")
    itens_venda = relationship("ItemVenda", back_populates="produto", cascade="all, delete-orphan")
    destaque = relationship("ProdutoDestaque", back_populates="produto")

    def calcular_preco_final(self):
        preco_decimal = Decimal(str(self.preco))
        margem_decimal = Decimal(self.margem_lucro) / Decimal(100) + Decimal(1)
        return preco_decimal * margem_decimal

    def atualizar_preco_final(self):
        self.preco_final = self.calcular_preco_final()

    @property
    def promocao_ativa(self):
        agora = datetime.utcnow()
        return next(
            (promo for promo in self.promocoes if promo.ativo and promo.data_inicio <= agora <= promo.data_fim),
            None
        )

    @property
    def preco_com_promocao(self):
        promocao = self.promocao_ativa
        if promocao:
            if promocao.preco_promocional:
                return promocao.preco_promocional
            elif promocao.desconto_percentual:
                desconto = self.preco_final * (promocao.desconto_percentual / Decimal(100))
                return self.preco_final - desconto
        return self.preco_final

    @property
    def tem_promocao_ativa(self) -> bool:
        """Verifica se o produto está em promoção ativa."""
        return self.promocao_ativa is not None

    def __repr__(self):
        return f"<Produto(id={self.id}, nome='{self.nome}', sku='{self.sku}')>"
