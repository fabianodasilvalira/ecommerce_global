from pydantic import BaseModel, condecimal
from enum import Enum

from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from app.schemas.usuario_schema import UsuarioOut
from app.schemas.endereco import EnderecoOut
from app.schemas.cupom_schema import CupomOut
from app.schemas.item_venda_schema import ItemVendaOut


class StatusVendaEnum(str, Enum):
    PENDENTE = "pendente"
    PAGO = "pago"
    CANCELADO = "cancelado"


class ItemVendaCreate(BaseModel):
    produto_id: int
    quantidade: int


class VendaCreate(BaseModel):
    endereco_id: Optional[int]
    cupom_id: Optional[int]
    itens: List[ItemVendaCreate]


class ItemVendaResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: condecimal(max_digits=10, decimal_places=2)

    class Config:
        orm_mode = True


class VendaResponse(BaseModel):
    id: int
    usuario_id: int
    endereco_id: Optional[int]
    cupom_id: Optional[int]
    total: condecimal(max_digits=10, decimal_places=2)
    status: StatusVendaEnum
    data_venda: datetime
    itens: List[ItemVendaResponse]

    class Config:
        orm_mode = True


class VendaDetalhadaResponse(VendaResponse):
    # Pode-se adicionar mais campos específicos para o detalhamento aqui se necessário
    pass


class VendaOut(BaseModel):
    id: int
    usuario: UsuarioOut
    endereco: EnderecoOut
    cupom: Optional[CupomOut]
    total: Decimal
    status: str
    data_venda: datetime
    itens: List[ItemVendaOut]

    class Config:
        orm_mode = True