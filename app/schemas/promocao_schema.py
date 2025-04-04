from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import Optional

class PromocaoBase(BaseModel):
    produto_id: int
    desconto_percentual: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    preco_promocional: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    data_inicio: datetime
    data_fim: datetime
    ativo: Optional[bool] = True

class PromocaoCreate(PromocaoBase):
    pass

class PromocaoUpdate(BaseModel):
    desconto_percentual: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    preco_promocional: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    ativo: Optional[bool] = None

class PromocaoResponse(PromocaoBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
