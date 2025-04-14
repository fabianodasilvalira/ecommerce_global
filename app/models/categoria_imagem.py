from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.database import Base
from enum import Enum


class TipoImagemCategoria(str, Enum):
    DESTAQUE = "destaque"
    THUMBNAIL = "thumbnail"
    BANNER = "banner"


class CategoriaImagem(Base):
    __tablename__ = "categoria_imagem"

    id = Column(Integer, primary_key=True, index=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="CASCADE"), nullable=False)
    imagem_url = Column(String(500), nullable=False)
    tipo = Column(String(50), nullable=False, default=TipoImagemCategoria.DESTAQUE)
    ordem = Column(Integer, nullable=False, default=0)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    categoria = relationship("Categoria", back_populates="imagens")

    def __repr__(self):
        return f"<CategoriaImagem(id={self.id}, tipo='{self.tipo}')>"
