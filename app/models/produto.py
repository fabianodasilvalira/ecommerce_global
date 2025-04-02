from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


# Modelo de Produto
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=True)
    preco = Column(Float, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=True)

    categoria = relationship("Categoria")
    imagens = relationship("ProdutoImagem", back_populates="produto")
    estoque = relationship("Estoque", uselist=False, back_populates="produto")
