from sqlalchemy import Column, Integer, Enum, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class EntregadorInfo(Base):
    __tablename__ = "entregador_info"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), unique=True)
    placa = Column(String(10), nullable=True)
    cnh = Column(String(20), nullable=True)
    endereco = Column(String(255), nullable=True)

    usuario = relationship("Usuario", backref="entregador_info")
