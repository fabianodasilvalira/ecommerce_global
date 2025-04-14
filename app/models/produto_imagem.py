from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, Enum, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.db.database import Base


# Enum para tipos de imagem
class TipoImagemProduto(PyEnum):
    DESTAQUE = "DESTAQUE"
    GALERIA = "GALERIA"
    THUMBNAIL = "THUMBNAIL"
    ZOOM = "ZOOM"


class ProdutoImagem(Base):
    __tablename__ = "produto_imagem"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produto.id", ondelete="CASCADE"), nullable=False)
    imagem_url = Column(String(500), nullable=False)
    tipo = Column(Enum(TipoImagemProduto), nullable=False, default=TipoImagemProduto.GALERIA)
    ordem = Column(Integer, nullable=True)
    visivel = Column(Boolean, default=True)  # imagem ativa ou não
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    atualizado_em = Column(TIMESTAMP, onupdate=func.now(), nullable=True)  # ✅ ESSENCIAL

    produto = relationship("Produto", back_populates="imagens")

    __table_args__ = (
        Index('ix_produto_id_ordem', 'produto_id', 'ordem'),
    )
