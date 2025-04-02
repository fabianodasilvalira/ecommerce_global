from pydantic import BaseModel
from typing import Optional


class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    categoria_id: int  # Ajustado para inteiro


class ProdutoResponse(ProdutoCreate):
    id: int
    sku: str
    preco_final: float

    class Config:
        from_attributes = True


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    categoria_id: Optional[int] = None
    ativo: Optional[bool] = None
    volume: Optional[float] = None
    unidade_medida: Optional[str] = None
