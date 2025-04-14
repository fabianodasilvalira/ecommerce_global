from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ProdutoDestaqueBase(BaseModel):
    produto_id: int = Field(..., description="ID do produto a ser destacado")
    posicao: Optional[int] = Field(None, description="Posição de exibição")
    tipo_destaque: Optional[str] = Field('principal', description="Tipo de destaque")


class ProdutoDestaqueCreate(ProdutoDestaqueBase):
    pass


class ProdutoDestaqueUpdate(BaseModel):
    posicao: Optional[int] = None
    ativo: Optional[bool] = None
    tipo_destaque: Optional[str] = None


class ProdutoDestaqueResponse(ProdutoDestaqueBase):
    id: int
    criado_em: datetime
    ativo: bool

    class Config:
        from_attributes = True


class ProdutoDestaqueComProduto(ProdutoDestaqueResponse):
    produto: dict  # Ou use um schema de produto se já tiver