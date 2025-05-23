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
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf_cnpj: Optional[str] = None
    telefone: Optional[str] = None
    tipo_usuario: Optional[TipoUsuarioEnum] = None
    senha: Optional[str] = None
    ativo: Optional[bool]  # 👈 Adicione este campo

    class Config:
        orm_mode = True


class UsuarioUpdateAdmin(UsuarioUpdate):
    pass  # Herda tudo de UsuarioUpdate


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
