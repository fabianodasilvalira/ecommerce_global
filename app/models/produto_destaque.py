from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class ProdutoDestaque(Base):
    __tablename__ = "produto_destaque"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produto.id"), nullable=False, unique=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    produto = relationship("Produto", back_populates="destaque")
