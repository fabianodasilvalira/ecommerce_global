from pydantic import BaseModel
from typing import Optional


class ProdutoCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    categoria_id: int  # Certifique-se de que você está usando categoria_id aqui
    volume: Optional[float] = None
    unidade_medida: Optional[str] = 'ml'
    ativo: Optional[bool] = True


class ProdutoResponse(BaseModel):
    id: int
    sku: str
    nome: str
    descricao: str
    preco: float
    volume: Optional[float] = None  # Atualizado para ser opcional, como na sua lógica
    unidade_medida: str
    ativo: bool
    categoria_id: int
    preco_final: float  # Adicionando o campo preco_final

    class Config:
        orm_mode = True


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    categoria_id: Optional[int] = None
    ativo: Optional[bool] = None
    volume: Optional[float] = None
    unidade_medida: Optional[str] = None
