from decimal import Decimal

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.produto_schema import ProdutoOut

class CupomCreate(BaseModel):
    codigo: str = Field(..., max_length=50)
    desconto: float = Field(..., gt=0)
    validade: datetime
    ativo: bool = True

class CupomUpdate(BaseModel):
    desconto: Optional[float] = Field(None, gt=0)
    validade: Optional[datetime] = None
    ativo: Optional[bool] = None

class CupomResponse(BaseModel):
    id: int
    codigo: str
    desconto: float
    validade: datetime
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True



class CupomOut(BaseModel):
    id: int
    codigo: str
    desconto: float

    class Config:
        orm_mode = True