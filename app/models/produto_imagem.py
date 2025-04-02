from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class ProdutoImagem(Base):
    __tablename__ = "produto_imagem"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produto.id", ondelete="CASCADE"), nullable=False)
    imagem_url = Column(String(255), nullable=False)

    produto = relationship("Produto", back_populates="imagens")
