from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

# Modelo de Promoção
class Promocao(Base):
    __tablename__ = "promocao"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produto.id", ondelete="CASCADE"), nullable=False, index=True)
    desconto = Column(DECIMAL(5,2), nullable=False)  # Melhor precisão
    data_inicio = Column(TIMESTAMP, nullable=False)
    data_fim = Column(TIMESTAMP, nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)  # Novo

    produto = relationship("Produto", cascade="all, delete")

    __table_args__ = (
        CheckConstraint("desconto >= 0 AND desconto <= 100", name="check_desconto"),
    )
