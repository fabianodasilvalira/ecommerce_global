# app/models/categoria.py
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Categoria(Base):
    __tablename__ = "categorias"  # Mantendo o nome no plural

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False)
    descricao = Column(Text, nullable=True)
    imagem_url = Column(String(255), nullable=True)
    cor_destaque = Column(String(7), nullable=True)
    ativo = Column(Boolean, default=True)

    # Adicionando o relacionamento de volta para Produto
    produtos = relationship("Produto", back_populates="categoria")