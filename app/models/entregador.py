from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base

class Entregador(Base):
    __tablename__ = "entregador"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    entregas_candidatadas = relationship("EntregaCandidato", back_populates="entregador", cascade="all, delete-orphan")
