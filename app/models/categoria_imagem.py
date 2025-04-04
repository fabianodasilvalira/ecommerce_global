from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class CategoriaImagem(Base):
    __tablename__ = "categoria_imagem"

    id = Column(Integer, primary_key=True, index=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="CASCADE"), nullable=False)
    imagem_url = Column(String(500), nullable=False)
    tipo = Column(String(50), nullable=False, default="destaque")
    ordem = Column(Integer, nullable=True)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # Relacionamento (usando string para referência)
    categoria = relationship(
        "Categoria",
        back_populates="imagens"
    )

    def __repr__(self):
        return f"<CategoriaImagem(id={self.id}, tipo='{self.tipo}')>"