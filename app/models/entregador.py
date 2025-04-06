from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Entregador(Base):
    __tablename__ = "entregador"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
