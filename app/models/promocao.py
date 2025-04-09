from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, TIMESTAMP, Boolean, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class Promocao(Base):
    __tablename__ = "promocao"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produto.id", ondelete="CASCADE"), nullable=False, index=True)
    desconto_percentual = Column(DECIMAL(5, 2), nullable=True)
    preco_promocional = Column(DECIMAL(10, 2), nullable=True)
    data_inicio = Column(TIMESTAMP, nullable=False)
    data_fim = Column(TIMESTAMP, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    produto = relationship("Produto", back_populates="promocoes")

    __table_args__ = (
        CheckConstraint("desconto_percentual >= 0 AND desconto_percentual <= 100", name="check_desconto"),
        CheckConstraint("preco_promocional IS NULL OR preco_promocional > 0", name="check_preco_promocional"),
        CheckConstraint("data_fim > data_inicio", name="check_datas_promocao"),
    )

    def esta_ativa(self) -> bool:
        """Verifica se a promoção está ativa considerando o período e status."""
        agora = datetime.utcnow()
        return self.ativo and self.data_inicio <= agora <= self.data_fim
