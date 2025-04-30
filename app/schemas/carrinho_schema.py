from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from app.models import ItemCarrinho
from app.models.pagamento import MetodoPagamentoEnum
from app.schemas.item_carrinho_schema import ItemCarrinhoPydantic
from app.schemas.produto_schema import ProdutoOut


class ItemCarrinhoInput(BaseModel):
    produto_id: int
    quantidade: int


class CarrinhoAtualizarInput(BaseModel):
    usuario_id: int  # necessário para associar o carrinho ao usuário que está atualizando
    itens: List[ItemCarrinhoInput]


class ItemCarrinhoBase(BaseModel):
    produto_id: int
    quantidade: int


class ItemCarrinhoOut(BaseModel):
    id: int
    quantidade: int
    valor_unitario: float
    valor_total: float
    produto: ProdutoOut
    preco_final: Optional[float] = None

    class Config:
        orm_mode = True


class CarrinhoOut(BaseModel):
    id: int
    usuario_id: int
    is_finalizado: bool
    itens: List[ItemCarrinhoOut]
    subtotal: float
    data_finalizacao: Optional[datetime]

    class Config:
        orm_mode = True


class CarrinhoResponse(BaseModel):
    id: int
    usuario_id: int
    is_finalizado: bool
    itens: List[ItemCarrinhoOut]
    subtotal: float
    total: float
    data_finalizacao: Optional[datetime]

    class Config:
        orm_mode = True


class FinalizarCarrinhoRequest(BaseModel):
    endereco_id: int
    cupom_id: Optional[int] = None
    itens: List[ItemCarrinhoPydantic]
    metodo_pagamento: MetodoPagamentoEnum
    numero_parcelas: Optional[int] = None  # Alterado para int
    bandeira_cartao: Optional[str] = None
    ultimos_digitos_cartao: Optional[str] = None
    nome_cartao: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True  # Permite tipos arbitrários como ItemCarrinho