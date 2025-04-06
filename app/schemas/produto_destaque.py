from pydantic import BaseModel
from datetime import datetime

class ProdutoDestaqueBase(BaseModel):
    produto_id: int

class ProdutoDestaqueCreate(ProdutoDestaqueBase):
    pass

class ProdutoDestaqueResponse(BaseModel):
    id: int
    produto_id: int
    criado_em: datetime

    class Config:
        from_attributes = True
