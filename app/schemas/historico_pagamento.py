from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class StatusHistoricoPagamento(str, Enum):
    PENDENTE = "PENDENTE"
    AUTORIZADO = "AUTORIZADO"
    FALHOU = "FALHOU"
    CANCELADO = "CANCELADO"
    ESTORNADO = "ESTORNADO"

class HistoricoPagamentoBase(BaseModel):
    status: StatusHistoricoPagamento
    metodo_pagamento: Optional[str] = None
    observacao: Optional[str] = None

class HistoricoPagamentoCreate(HistoricoPagamentoBase):
    pagamento_id: int

class HistoricoPagamentoResponse(HistoricoPagamentoBase):
    id: int
    pagamento_id: int
    data_evento: datetime

    class Config:
        orm_mode = True
