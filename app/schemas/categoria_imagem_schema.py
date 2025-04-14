from pydantic import BaseModel, HttpUrl, Field, validator
from datetime import datetime
from enum import Enum

class TipoImagemCategoria(str, Enum):
    DESTAQUE = "destaque"
    THUMBNAIL = "thumbnail"
    BANNER = "banner"

class CategoriaImagemBase(BaseModel):
    imagem_url: HttpUrl = Field(
        ...,
        description="URL da imagem (deve ser um link válido com http ou https)",
        example="https://cdn.suaempresa.com/imagens/categoria1-banner.jpg"
    )
    tipo: TipoImagemCategoria = Field(
        ...,
        description="Tipo da imagem da categoria",
        example="banner"
    )
    ordem: int = Field(
        0,
        description="Ordem da imagem no conjunto (0 = primeira)",
        example=1
    )

class CategoriaImagemCreate(CategoriaImagemBase):
    categoria_id: int = Field(
        ...,
        description="ID da categoria à qual esta imagem está associada",
        example=12
    )

class CategoriaImagemResponse(CategoriaImagemBase):
    id: int = Field(..., description="ID único da imagem", example=101)
    categoria_id: int = Field(..., description="ID da categoria relacionada", example=12)
    criado_em: str = Field(..., description="Data de criação da imagem", example="2025-04-14T10:15:30")

    @validator('criado_em', pre=True)
    def format_criado_em(cls, v):
        if isinstance(v, datetime):
            # Converte o datetime para o formato de string desejado (por exemplo, ISO 8601)
            return v.strftime("%Y-%m-%dT%H:%M:%S")
        return v

    class Config:
        orm_mode = True  # Permite retorno de objetos ORM diretamente

class CategoriaImagemReorder(BaseModel):
    id: int
    nova_ordem: int

    class Config:
        orm_mode = True
