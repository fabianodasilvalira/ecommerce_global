from pydantic import BaseModel, Field
from typing import Optional


class CategoriaBase(BaseModel):
    nome: str
    slug: str = Field(..., pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
    descricao: Optional[str] = None
    imagem_url: Optional[str] = None
    cor_destaque: Optional[str] = Field(None, pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    ordem: int = 0
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    ativo: bool = True


class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None
    slug: Optional[str] = Field(None, pattern=r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
    descricao: Optional[str] = None
    imagem_url: Optional[str] = None
    cor_destaque: Optional[str] = Field(None, pattern=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
    ordem: Optional[int] = None
    ativo: Optional[bool] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class CategoriaResponse(CategoriaBase):
    id: int
    ativo: bool
    produtos_count: Optional[int] = 0

    class Config:
        from_attributes = True


class CategoriaSimpleResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    ativo: bool

    class Config:
        from_attributes = True