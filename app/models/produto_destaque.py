from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class ProdutoDestaque(Base):
    __tablename__ = "produto_destaque"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produto.id"), nullable=False, unique=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    posicao = Column(Integer, nullable=True, comment="Ordem de exibição no destaque")
    ativo = Column(Boolean, default=True)
    tipo_destaque = Column(
        String(20),
        default='principal',
        comment="Tipos: 'principal', 'secundario', 'promocional', 'novidade', 'oferta'"
    )

    # Relacionamento
    produto = relationship("Produto", back_populates="destaque")

    def __repr__(self):
        return (
            f"<ProdutoDestaque(id={self.id}, produto_id={self.produto_id}, "
            f"posicao={self.posicao}, ativo={self.ativo}, tipo_destaque='{self.tipo_destaque}')>"
        )