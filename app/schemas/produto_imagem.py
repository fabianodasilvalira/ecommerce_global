from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class ProdutoImagemBase(BaseModel):
    produto_id: int
    imagem_url: HttpUrl
    tipo: Optional[str] = "galeria"
    ordem: Optional[int] = None


class ProdutoImagemCreate(ProdutoImagemBase):
    pass


class ProdutoImagemResponse(BaseModel):
    id: int
    produto_id: int
    imagem_url: HttpUrl
    tipo: str
    ordem: Optional[int]
    criado_em: datetime

    class Config:
        from_attributes = True


class ProdutoImagemOut(BaseModel):
    id: int
    imagem_url: HttpUrl
    tipo: Optional[str] = None
    ordem: Optional[int] = None

    class Config:
        from_attributes = True
