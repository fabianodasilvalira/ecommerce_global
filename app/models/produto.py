from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=True)
    preco = Column(DECIMAL(10, 2), nullable=False)
    volume = Column(Float, nullable=True)
    unidade_medida = Column(String(10), nullable=True, default="ml")
    ativo = Column(Boolean, default=True)

    # Corrigido para referenciar 'categorias.id' (plural)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)

    # Relacionamentos
    categoria = relationship("Categoria", back_populates="produtos")
    imagens = relationship("ProdutoImagem", back_populates="produto", cascade="all, delete-orphan")
    estoque = relationship("Estoque", uselist=False, back_populates="produto", cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="produto", cascade="all, delete-orphan")
    promocoes = relationship("Promocao", back_populates="produto", cascade="all, delete-orphan")

    @property
    def preco_final(self):
        """Retorna o menor preço entre o preço original e o promocional ativo."""
        promocao_ativa = next(
            (p for p in self.promocoes
             if p.ativo and p.data_inicio <= func.now() and p.data_fim >= func.now()),
            None
        )
        if promocao_ativa and promocao_ativa.preco_promocional:
            return min(float(self.preco), float(promocao_ativa.preco_promocional))
        return self.preco