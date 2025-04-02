from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum

# Modelo de Cupom de Desconto
class Cupom(Base):
    __tablename__ = "cupom"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)
    desconto = Column(Float, nullable=False)
    validade = Column(TIMESTAMP, nullable=False)
