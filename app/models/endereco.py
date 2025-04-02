from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


# Modelo de Endereço
class Endereco(Base):
    __tablename__ = "endereco"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(10))
    cidade = Column(String(100), nullable=False)
    estado = Column(String(50), nullable=False)
    cep = Column(String(20), nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now(), nullable=False)  # Opcional

    usuario = relationship("Usuario")
