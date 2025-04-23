from pydantic import BaseModel, condecimal, root_validator
from datetime import datetime
from typing import Optional

class PromocaoCreate(BaseModel):
    produto_id: int
    desconto_percentual: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    preco_promocional: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    data_inicio: datetime
    data_fim: datetime
    ativo: Optional[bool] = True

    @root_validator(pre=True)
    def verificar_desconto_ou_preco(cls, values):
        desconto_percentual = values.get('desconto_percentual')
        preco_promocional = values.get('preco_promocional')
        if not desconto_percentual and not preco_promocional:
            raise ValueError('Deve ser informado ao menos o desconto percentual ou o preço promocional')
        return values

class PromocaoUpdate(BaseModel):
    desconto_percentual: Optional[condecimal(max_digits=5, decimal_places=2)] = None
    preco_promocional: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    ativo: Optional[bool] = None

class PromocaoResponse(BaseModel):
    id: int
    descricao: Optional[str] = None
    preco_promocional: Optional[float] = None
    desconto_percentual: Optional[float] = None
    data_inicio: datetime
    data_fim: datetime
    ativo: bool

    class Config:
        orm_mode = True  # Permite que os objetos ORM sejam convertidos em Pydantic models


class PromocaoOut(PromocaoResponse):
    produto_id: int  # Produto ao qual a promoção está vinculada
    produto_nome: Optional[str] = None  # Nome do produto, caso necessário
    preco_original: Optional[float] = None  # Preço original do produto, se desejado
    # Outros campos que forem necessários, como o tipo de promoção, etc.

    class Config:
        orm_mode = True  # Permite conversão ORM -> Pydantic