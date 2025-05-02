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

    class Config:
        from_attributes = True  # Adicione essa linha!


class CarrinhoOut(BaseModel):
    id: int
    usuario_id: int
    is_finalizado: bool
    itens: List[ItemCarrinhoOut]
    subtotal: float
    data_finalizacao: Optional[datetime]

    class Config:
        from_attributes = True  # Adicione essa linha!


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
    itens: List[ItemCarrinhoInput]
    cupom_id: Optional[int] = None
    metodo_pagamento: MetodoPagamentoEnum
    numero_parcelas: Optional[int] = None
    bandeira_cartao: Optional[str] = None
    ultimos_digitos_cartao: Optional[str] = None
    nome_cartao: Optional[str] = None