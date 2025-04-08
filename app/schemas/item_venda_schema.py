# app/schemas/item_venda_schema.py

from pydantic import BaseModel
from decimal import Decimal
from app.schemas.produto_schema import ProdutoOut

class ItemVendaOut(BaseModel):
    id: int
    quantidade: int
    preco_unitario: Decimal
    produto: ProdutoOut

    class Config:
        orm_mode = True
