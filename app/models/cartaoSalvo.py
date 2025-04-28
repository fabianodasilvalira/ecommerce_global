from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class CartaoSalvo(Base):
    __tablename__ = "cartao_salvo"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)

    token = Column(String(255), nullable=False)            # Token seguro do cartão gerado pelo gateway
    bandeira = Column(String(50), nullable=False)           # Ex.: Visa, MasterCard
    ultimos_digitos = Column(String(4), nullable=False)     # Últimos 4 dígitos
    nome_impresso = Column(String(100), nullable=True)      # Nome do cartão (opcional)
    validade_mes = Column(Integer, nullable=True)           # Mês de validade
    validade_ano = Column(Integer, nullable=True)           # Ano de validade

    # Campos de controle
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    atualizado_em = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relacionamento
    usuario = relationship("Usuario", back_populates="cartoes")