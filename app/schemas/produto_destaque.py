from pydantic import BaseModel
from datetime import datetime

from app.schemas.produto_schema import ProdutoResponse


class ProdutoDestaqueBase(BaseModel):
    produto_id: int

class ProdutoDestaqueCreate(ProdutoDestaqueBase):
    pass

class ProdutoDestaqueResponse(BaseModel):
    id: int
    criado_em: datetime
    produto_id: int
    produto: ProdutoResponse  # novo campo com os dados do produto

    class Config:
        orm_mode = True
