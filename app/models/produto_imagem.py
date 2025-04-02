from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class ProdutoImagem(Base):
    __tablename__ = "produto_imagem"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produto.id", ondelete="CASCADE"), nullable=False)
    imagem_url = Column(String(500), nullable=False)
    tipo = Column(String(50), nullable=False, default="galeria")
    ordem = Column(Integer, nullable=True)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    produto = relationship("Produto", back_populates="imagens")  # Aqui deve ser "Produto"
