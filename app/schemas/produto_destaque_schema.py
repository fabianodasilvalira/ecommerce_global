from pydantic import BaseModel
from datetime import datetime

from app.schemas.produto_schema import ProdutoResponse


class ProdutoDestaqueBase(BaseModel):
    produto_id: int

class ProdutoDestaqueCreate(ProdutoDestaqueBase):
    pass

class ProdutoDestaqueResponse(BaseModel):
    id: int
    produto: ProdutoResponse  # Embed full product data

    class Config:
        from_attributes = True
