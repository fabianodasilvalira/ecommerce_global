from pydantic import BaseModel, constr, condecimal
from typing import Optional
from datetime import datetime
from enum import Enum as PydanticEnum


# Enum para os métodos de pagamento
class MetodoPagamentoEnum(str, PydanticEnum):
    PIX = "PIX"
    CARTAO_CREDITO = "CARTAO_CREDITO"
    CARTAO_DEBITO = "CARTAO_DEBITO"
    BOLETO = "BOLETO"
    CARTEIRA_DIGITAL = "CARTEIRA_DIGITAL"


# Enum para os status de pagamento
class StatusPagamento(str, PydanticEnum):
    PENDENTE = "PENDENTE"
    EM_ANALISE = "EM_ANALISE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"
    CANCELADO = "CANCELADO"
    ESTORNADO = "ESTORNADO"


# Modelo base de pagamento
class PagamentoBase(BaseModel):
    venda_id: int
    valor: condecimal(max_digits=10, decimal_places=2)  # Limite de dígitos e casas decimais
    metodo_pagamento: MetodoPagamentoEnum
    transacao_id: Optional[constr(max_length=100)] = None  # Opcional, mas se fornecido, será string de até 100 caracteres


# Modelo para criar um pagamento
class PagamentoCreate(PagamentoBase):
    pass


# Modelo para atualizar um pagamento
class PagamentoUpdate(BaseModel):
    status: Optional[StatusPagamento] = None  # Status do pagamento que pode ser atualizado
    transacao_id: Optional[constr(max_length=100)] = None  # Transação opcionalmente atualizada


# Modelo para resposta ao usuário com os dados do pagamento
class PagamentoResponse(PagamentoBase):
    id: int
    status: StatusPagamento
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True  # Configuração importante para que o Pydantic converta SQLAlchemy para Pydantic
