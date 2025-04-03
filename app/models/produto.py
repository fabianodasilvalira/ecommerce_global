from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float, Boolean
from sqlalchemy.orm import relationship
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

    # Chave estrangeira corrigida (note que a tabela de categoria é 'categorias')
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="SET NULL"), nullable=True)

    # Relacionamentos usando string references
    imagens = relationship("ProdutoImagem", back_populates="produto", lazy="joined", cascade="all, delete-orphan")
    estoque = relationship("Estoque", back_populates="produto", uselist=False, cascade="all, delete-orphan")
    avaliacoes = relationship("Avaliacao", back_populates="produto", cascade="all, delete-orphan")  # Atualizado
    promocoes = relationship("Promocao", back_populates="produto", cascade="all, delete-orphan")
    categoria = relationship("Categoria", back_populates="produtos")
    itens_venda = relationship("ItemVenda", back_populates="produto", cascade="all, delete-orphan")
