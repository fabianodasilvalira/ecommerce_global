from pydantic import BaseModel
from typing import List
from app.schemas.produto_schema import ProdutoOut


class ItemCarrinhoBase(BaseModel):
    produto_id: int
    quantidade: int


class ItemCarrinhoOut(BaseModel):
    id: int
    quantidade: int
    valor_unitario: float
    valor_total: float
    produto: ProdutoOut  # dados do produto embutido

    class Config:
        orm_mode = True


class CarrinhoOut(BaseModel):
    id: int
    usuario_id: int
    is_finalizado: bool
    itens: List[ItemCarrinhoOut]
    subtotal: float  # campo adicional com o valor total do carrinho

    class Config:
        orm_mode = True
