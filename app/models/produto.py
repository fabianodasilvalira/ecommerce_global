from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float, Boolean
from sqlalchemy.orm import relationship
from decimal import Decimal

from app.db.database import Base

class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=True)
    preco = Column(DECIMAL(10, 2), nullable=False)  # Preço de custo
    volume = Column(Float, nullable=True)
    unidade_medida = Column(String(10), nullable=True)
    ativo = Column(Boolean, default=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="SET NULL"), nullable=True)
    margem_lucro = Column(DECIMAL(5, 2), nullable=False, default=20.00)  # Corrigido parêntese
    preco_final = Column(DECIMAL(10, 2), nullable=False)  # Adicionando preco_final

    # Relacionamentos
    imagens = relationship("ProdutoImagem", back_populates="produto", lazy="joined", cascade="all, delete-orphan")
    estoque = relationship("Estoque", back_populates="produto", uselist=False, cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="produto", cascade="all, delete-orphan")
    promocoes = relationship("Promocao", back_populates="produto", cascade="all, delete-orphan")
    categoria = relationship("Categoria", back_populates="produtos")
    itens_venda = relationship("ItemVenda", back_populates="produto", cascade="all, delete-orphan")
    destaque = relationship("ProdutoDestaque", back_populates="produto")

    def calcular_preco_final(self):
        """Calcula o preço final do produto baseado na margem de lucro."""
        preco_decimal = Decimal(str(self.preco))  # Converte para Decimal
        margem_decimal = Decimal(self.margem_lucro) / Decimal(100) + Decimal(1)
        return preco_decimal * margem_decimal

    def atualizar_preco_final(self):
        """Atualiza o campo preco_final no banco de dados."""
        self.preco_final = self.calcular_preco_final()

    def __repr__(self):
        return f"<Produto(id={self.id}, nome='{self.nome}', sku='{self.sku}')>"
