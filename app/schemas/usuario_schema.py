from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime


class TipoUsuarioEnum(str, Enum):
    CLIENTE = "cliente"
    ADMIN = "admin"
    FUNCIONARIO = "funcionario"
    ENTREGADOR = "entregador"


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    cpf_cnpj: str
    telefone: Optional[str] = None
    tipo_usuario: TipoUsuarioEnum


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioUpdate(BaseModel):
    nome: Optional[str]
    telefone: Optional[str]
    senha: Optional[str]
    tipo_usuario: Optional[TipoUsuarioEnum]


class UsuarioOut(UsuarioBase):
    id: int
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True
