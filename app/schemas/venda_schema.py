from pydantic import BaseModel, condecimal
from enum import Enum

from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from app.schemas.usuario_schema import UsuarioOut
from app.schemas.endereco import EnderecoOut
from app.schemas.cupom_schema import CupomOut
from app.schemas.promocao_schema import PromocaoOut
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
    cupom_id: Optional[int] = None
    itens: List[ItemVendaCreate]


class ItemVendaResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: condecimal(max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True


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
        from_attributes = True  # Corrigido aqui também


class VendaDetalhadaResponse(VendaResponse):
    pass  # Herda de VendaResponse, já configurado corretamente


class VendaOut(BaseModel):
    id: int
    usuario: UsuarioOut
    endereco: EnderecoOut
    cupom: Optional[CupomOut] = None  # Explicitamente None como default
    promocoes: Optional[List[PromocaoOut]] = None  # Mudado para None
    total: Decimal
    status: str
    data_venda: datetime
    itens: List[ItemVendaOut]
    carrinho_id: Optional[int] = None
    carrinho: Optional[dict] = None

    class Config:
        from_attributes = True  # Usar apenas esta opção (orm_mode está deprecated)

    @classmethod
    def from_orm(cls, obj):
        # Garantir que promocoes seja None se não existir
        promocoes = None
        if hasattr(obj, 'promocoes') and obj.promocoes:
            # Se o objeto 'promocoes' existir e contiver dados, converta cada promoção
            promocoes = [PromocaoOut.from_orm(p) for p in obj.promocoes]

        # Construa o dicionário manualmente para maior controle
        venda_data = {
            "id": obj.id,
            "usuario": UsuarioOut.from_orm(obj.usuario),
            "endereco": EnderecoOut.from_orm(obj.endereco),
            "cupom": CupomOut.from_orm(obj.cupom) if obj.cupom else None,
            "promocoes": promocoes,  # Agora incluímos promocoes diretamente
            "total": obj.total,
            "status": obj.status,
            "data_venda": obj.data_venda,
            "itens": [ItemVendaOut.from_orm(i) for i in obj.itens],
            "carrinho_id": obj.carrinho_id,
            "carrinho": None  # Inicialmente None
        }

        # Processa carrinho apenas se existir
        if hasattr(obj, 'carrinho') and obj.carrinho:
            venda_data["carrinho"] = {
                "id": obj.carrinho.id,
                "criado_em": obj.carrinho.criado_em,
                "finalizado_em": obj.carrinho.atualizado_em
            }

        return cls(**venda_data)
