from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

from app.schemas.produto_schema import ProdutoResponse


# Definindo o Enum de Tipos de Destaque
class TipoDestaqueEnum(str, Enum):
    principal = "principal"
    secundario = "secundario"
    promocional = "promocional"
    novidade = "novidade"
    oferta = "oferta"


# Modelo base para ProdutoDestaque
class ProdutoDestaqueBase(BaseModel):
    produto_id: int = Field(..., description="ID do produto a ser destacado")
    posicao: Optional[int] = Field(None, description="Posição de exibição (1-99)")
    tipo_destaque: Optional[TipoDestaqueEnum] = Field(
        TipoDestaqueEnum.principal,
        description="Tipo de destaque. Opções possíveis: 'principal', 'secundario', 'promocional', 'novidade', 'oferta'"
    )

    # Validação para garantir que a posição esteja entre 1 e 99
    @validator('posicao')
    def validar_posicao(cls, v):
        if v is not None and (v < 1 or v > 99):
            raise ValueError("A posição deve estar entre 1 e 99")
        return v


# Modelo para criação de um novo destaque
class ProdutoDestaqueCreate(ProdutoDestaqueBase):
    pass


# Modelo para atualização de destaque
class ProdutoDestaqueUpdate(BaseModel):
    posicao: Optional[int] = Field(None, description="Posição de exibição (1-99)")
    ativo: Optional[bool] = Field(None, description="Status do destaque (True ou False)")
    tipo_destaque: Optional[TipoDestaqueEnum] = Field(
        None,
        description="Tipo de destaque. Opções possíveis: 'principal', 'secundario', 'promocional', 'novidade', 'oferta'"
    )

    # Validação para garantir que a posição esteja entre 1 e 99
    @validator('posicao')
    def validar_posicao(cls, v):
        if v is not None and (v < 1 or v > 99):
            raise ValueError("A posição deve estar entre 1 e 99")
        return v


# Modelo de resposta para ProdutoDestaque
class ProdutoDestaqueResponse(ProdutoDestaqueBase):
    id: int
    criado_em: datetime
    ativo: bool

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# Modelo de resposta incluindo os detalhes do produto
class ProdutoDestaqueComProduto(ProdutoDestaqueResponse):
    produto: ProdutoResponse  # ✅ Corretamente incluindo a resposta do Produto

    class Config:
        from_attributes = True
