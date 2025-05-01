from dataclasses import Field

from pydantic import BaseModel, Field, validator, condecimal
from enum import Enum

from datetime import datetime
from typing import List, Optional
from decimal import Decimal

from app.models import Carrinho
from app.models.pagamento import MetodoPagamentoEnum
from app.schemas.carrinho_schema import CarrinhoOut
from app.schemas.pagamento_schema import PagamentoOut
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
    carrinho_id: Optional[int] = None
    metodo_pagamento: Optional[MetodoPagamentoEnum] = None
    nome_cartao: Optional[str] = None

    numero_parcelas: Optional[int] = Field(
        default=None,
        description="Número de parcelas (obrigatório para cartão de crédito)"
    )
    bandeira_cartao: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Bandeira do cartão (VISA, MASTERCARD, etc)"
    )
    ultimos_digitos_cartao: Optional[str] = Field(
        default=None,
        min_length=4,
        max_length=4,
        description="Últimos 4 dígitos do cartão"
    )

    @validator("numero_parcelas", always=True)
    def validate_parcelas(cls, v, values):
        metodo = values.get("metodo_pagamento")

        if metodo == MetodoPagamentoEnum.CARTAO_CREDITO:
            if v is None:
                raise ValueError("O número de parcelas é obrigatório para o método de pagamento selecionado.")
            try:
                v_int = int(v)
            except ValueError:
                raise ValueError("O número de parcelas deve ser um número inteiro.")
            if v_int < 1 or v_int > 12:
                raise ValueError("O número de parcelas deve estar entre 1 e 12.")
            return v_int
        return None if v is None else int(v)


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


from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

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
    pagamentos: Optional[List[PagamentoOut]] = None  # Adicionando pagamentos
    total_parcelas: Optional[int] = None  # Total de parcelas

    class Config:
        from_attributes = True  # Usar apenas esta opção (orm_mode está deprecated)

    @classmethod
    def from_orm(cls, obj):
        # Garantir que promocoes seja None se não existir
        promocoes = None
        if hasattr(obj, 'itens') and obj.itens:
            # Vamos usar a propriedade promocao_ativa do produto
            promocoes_ativas = [
                i.produto.promocao_ativa for i in obj.itens if i.produto.promocao_ativa
            ]

            if promocoes_ativas:
                # Converter as promoções ativas para o formato PromocaoOut
                promocoes = [PromocaoOut.from_orm(p) for p in promocoes_ativas]
            else:
                print("Nenhuma promoção ativa encontrada.")

        venda_data = {
            "id": obj.id,
            "usuario": UsuarioOut.from_orm(obj.usuario),
            "endereco": EnderecoOut.from_orm(obj.endereco),
            "cupom": CupomOut.from_orm(obj.cupom) if obj.cupom else None,
            "promocoes": promocoes,  # Agora retorna as promoções como PromocaoOut
            "total": obj.total,
            "status": obj.status,
            "data_venda": obj.data_venda,
            "itens": [ItemVendaOut.from_orm(i) for i in obj.itens],
            "carrinho_id": obj.carrinho_id,
            "carrinho": None
        }

        # Processa carrinho apenas se existir
        if hasattr(obj, 'carrinho') and obj.carrinho:
            venda_data["carrinho"] = {
                "id": obj.carrinho.id,
                "criado_em": obj.carrinho.criado_em,
                "finalizado_em": obj.carrinho.atualizado_em
            }

        # Adiciona os pagamentos, se existirem
        if hasattr(obj, 'pagamentos') and obj.pagamentos:
            venda_data["pagamentos"] = [
                PagamentoOut.from_orm(pagamento) for pagamento in obj.pagamentos
            ]
            # Calcular o total de parcelas
            venda_data["total_parcelas"] = max(pagamento.numero_parcelas for pagamento in obj.pagamentos)
        else:
            venda_data["pagamentos"] = None  # Caso contrário, setar como None
            venda_data["total_parcelas"] = 0  # Nenhuma parcela, então o total é 0

        return cls(**venda_data)


