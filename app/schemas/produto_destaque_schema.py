from pydantic import BaseModel
from datetime import datetime

class ProdutoDestaqueBase(BaseModel):
    produto_id: int

class ProdutoDestaqueCreate(ProdutoDestaqueBase):
    pass

class ProdutoDestaqueResponse(ProdutoDestaqueBase):
    id: int
    criado_em: datetime

    class Config:
        orm_mode = True
