from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    descricao = Column(Text, nullable=True)
    imagem_url = Column(String(255), nullable=True)
    cor_destaque = Column(String(7), nullable=True)
    ordem = Column(Integer, default=0)
    meta_title = Column(String(100), nullable=True)
    meta_description = Column(String(255), nullable=True)
    ativo = Column(Boolean, default=True)

    # Relacionamentos
    imagens = relationship(
        "CategoriaImagem",
        back_populates="categoria",
        cascade="all, delete-orphan"
    )

    produtos = relationship(
        "Produto",
        back_populates="categoria",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Categoria(id={self.id}, nome='{self.nome}')>"