from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

from app.schemas.produto_schema import ProdutoResponse


class TipoDestaqueEnum(str, Enum):
    principal = "principal"
    secundario = "secundario"
    promocional = "promocional"
    novidade = "novidade"
    oferta = "oferta"


class ProdutoDestaqueBase(BaseModel):
    produto_id: int = Field(..., description="ID do produto a ser destacado")
    posicao: Optional[int] = Field(None, description="Posição de exibição (1-99)")
    tipo_destaque: Optional[TipoDestaqueEnum] = Field(
        TipoDestaqueEnum.principal,
        description="Tipo de destaque"
    )

    @validator('posicao')
    def validar_posicao(cls, v):
        if v is not None and (v < 1 or v > 99):
            raise ValueError("A posição deve estar entre 1 e 99")
        return v


class ProdutoDestaqueCreate(ProdutoDestaqueBase):
    pass


class ProdutoDestaqueUpdate(BaseModel):
    posicao: Optional[int] = Field(None, description="Posição de exibição (1-99)")
    ativo: Optional[bool] = Field(None, description="Status do destaque")
    tipo_destaque: Optional[TipoDestaqueEnum] = Field(
        None,
        description="Tipo de destaque"
    )

    @validator('posicao')
    def validar_posicao(cls, v):
        if v is not None and (v < 1 or v > 99):
            raise ValueError("A posição deve estar entre 1 e 99")
        return v


class ProdutoDestaqueResponse(ProdutoDestaqueBase):
    id: int
    criado_em: datetime
    ativo: bool

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ProdutoDestaqueComProduto(ProdutoDestaqueResponse):
    produto: ProdutoResponse  # ✅ CORRETO AGORA

    class Config:
        from_attributes = True