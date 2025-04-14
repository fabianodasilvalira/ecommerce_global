from pydantic import BaseModel
from typing import Optional

class CategoriaCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    imagem_url: Optional[str] = None
    cor_destaque: Optional[str] = None
    ativo: bool = True

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    imagem_url: Optional[str] = None
    cor_destaque: Optional[str] = None
    ativo: Optional[bool] = None  # Agora aceita None corretamente


class CategoriaResponse(CategoriaCreate):
    id: int

    class Config:
        from_attributes = True


class CategoriaSimpleResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    ativo: bool

    class Config:
        from_attributes = True