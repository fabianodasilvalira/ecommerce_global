from decimal import Decimal

from pydantic import BaseModel
from typing import Optional


class ProdutoCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    categoria_id: int  # Certifique-se de que está correto
    volume: Optional[float] = None
    unidade_medida: Optional[str] = None  # Melhor manter None do que 'ml' por padrão
    ativo: Optional[bool] = True
    margem_lucro: Optional[float] = 20.0  # Margem de lucro com valor padrão


class ProdutoResponse(BaseModel):
    id: int
    sku: str
    nome: str
    descricao: str
    preco: float
    volume: Optional[float] = None  # Mantém consistência com ProdutoCreate
    unidade_medida: Optional[str] = None  # Evita usar string vazia como padrão
    ativo: bool
    categoria_id: int
    margem_lucro: float
    preco_final: float  # Preço final já calculado
    preco_com_promocao: Optional[Decimal]  # <- Adiciona isso aqui


    class Config:
        from_attributes = True  # ✅ Correção para Pydantic v2


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    volume: Optional[float] = None
    unidade_medida: Optional[str] = None
    ativo: Optional[bool] = None
    categoria_id: Optional[int] = None
    margem_lucro: Optional[float] = None


class ProdutoOut(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    imagem_url: str
    categoria: str

    class Config:
        orm_mode = True