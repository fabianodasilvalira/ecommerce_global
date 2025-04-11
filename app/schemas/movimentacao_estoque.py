from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class TipoMovimentacao(str, Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class MovimentacaoEstoqueBase(BaseModel):
    produto_id: int
    quantidade: int
    tipo_movimentacao: TipoMovimentacao

class MovimentacaoEstoqueCreate(MovimentacaoEstoqueBase):
    pass

class MovimentacaoEstoqueOut(MovimentacaoEstoqueBase):
    id: int
    data: datetime
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True
