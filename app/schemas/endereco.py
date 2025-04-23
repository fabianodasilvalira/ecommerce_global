from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime


class EnderecoBase(BaseModel):
    logradouro: str
    numero: str
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    estado: constr(min_length=2, max_length=2)
    cep: constr(min_length=8, max_length=9)


class EnderecoCreate(EnderecoBase):
    usuario_id: int


class EnderecoUpdate(EnderecoBase):
    ativo: Optional[bool] = None  # Permite atualizar se o endereço está ativo ou não


class EnderecoOut(BaseModel):
    id: int
    logradouro: str
    numero: str
    cidade: str

    class Config:
        from_attributes = True
