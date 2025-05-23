from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Boolean  # Adicione Boolean aqui
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
from datetime import datetime

class Cupom(Base):
    __tablename__ = "cupom"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)
    desconto = Column(Float, nullable=False)
    validade = Column(TIMESTAMP, nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now())
    ativo = Column(Boolean, default=True)

    # Relacionamento com Venda
    vendas = relationship("Venda", back_populates="cupom")

    @property
    def is_valido(self) -> bool:
        """Retorna True se o cupom estiver ativo e dentro do prazo de validade."""
        agora = datetime.utcnow()
        return self.ativo and self.validade > agora