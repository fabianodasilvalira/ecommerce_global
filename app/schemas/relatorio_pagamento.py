from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

# Mesmo Enum usado no model
class StatusPagamentoEnum(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    CANCELADO = "CANCELADO"

class FiltroRelatorioPagamento(BaseModel):
    metodo_pagamento: Optional[str] = None
    status: Optional[StatusPagamentoEnum] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
