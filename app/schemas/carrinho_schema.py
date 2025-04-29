from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from app.schemas.produto_schema import ProdutoOut

class ItemCarrinhoInput(BaseModel):
    produto_id: int
    quantidade: int

# Modelo para receber o corpo inteiro da requisição
class CarrinhoAtualizarInput(BaseModel):
    usuario_id: int
    itens: List[ItemCarrinhoInput]  # Lista de itens com produto_id e quantidade

class ItemCarrinhoBase(BaseModel):
    produto_id: int
    quantidade: int


class ItemCarrinhoOut(BaseModel):
    id: int
    quantidade: int
    valor_unitario: float
    valor_total: float
    produto: ProdutoOut  # Dados do produto embutido
    preco_final: Optional[float] = None  # Torne o campo opcional

    class Config:
        orm_mode = True


class CarrinhoOut(BaseModel):
    id: int
    usuario_id: int
    is_finalizado: bool
    itens: List[ItemCarrinhoOut]
    subtotal: float  # Campo adicional com o valor total do carrinho
    data_finalizacao: Optional[datetime]  # Adiciona este campo, pode ser None se não finalizado

    class Config:
        orm_mode = True


class CarrinhoResponse(BaseModel):
    id: int
    usuario_id: int
    is_finalizado: bool
    itens: List[ItemCarrinhoOut]  # Use o tipo correto (List[ItemCarrinhoOut] para consistência)
    subtotal: float
    total: float
    data_finalizacao: Optional[datetime]  # Agora é opcional, como esperado

    class Config:
        orm_mode = True
