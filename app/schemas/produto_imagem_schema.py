from typing import Optional

from pydantic import BaseModel, HttpUrl, Field, validator
from enum import Enum
from datetime import datetime

class TipoImagemProduto(str, Enum):
    DESTAQUE = "DESTAQUE"
    GALERIA = "GALERIA"
    THUMBNAIL = "THUMBNAIL"
    ZOOM = "ZOOM"

class ProdutoImagemBase(BaseModel):
    imagem_url: HttpUrl = Field(..., example="https://cdn.exemplo.com/imagem1.jpg")
    tipo: TipoImagemProduto = Field(default=TipoImagemProduto.GALERIA)
    ordem: int | None = Field(default=None, example=1)
    visivel: bool = Field(default=True)

class ProdutoImagemCreate(ProdutoImagemBase):
    produto_id: int = Field(..., example=42)

    def to_dict(self):
        return {
            "produto_id": self.produto_id,
            "imagem_url": str(self.imagem_url),
            "tipo": self.tipo.value,  # Garante que 'tipo' seja passado como maiúsculo
            "ordem": self.ordem,
            "visivel": self.visivel
        }

class ProdutoImagemResponse(BaseModel):
    id: int
    imagem_url: str
    produto_id: int
    tipo: str
    ordem: Optional[int] = None
    visivel: bool
    criado_em: str  # Mantém como string
    atualizado_em: Optional[str] = None

    @validator('criado_em', pre=True)
    def format_criado_em(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()  # Converte para string ISO 8601
        return value

    @validator('atualizado_em', pre=True)
    def format_atualizado_em(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    class Config:
        from_attributes = True


class ProdutoImagemUpdate(BaseModel):
    imagem_url: Optional[str] = None
    tipo: Optional[str] = None
    ordem: Optional[int] = None
    visivel: Optional[bool] = None
    atualizado_em: Optional[datetime] = None

