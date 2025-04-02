from pydantic import BaseModel, EmailStr
from enum import Enum

class TipoUsuarioEnum(str, Enum):
    CLIENTE = "CLIENTE"
    ADMIN = "ADMIN"
    FUNCIONARIO = "FUNCIONARIO"
    ENTREGADOR = "ENTREGADOR"

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    cpf_cnpj: str
    telefone: str | None = None
    tipo_usuario: TipoUsuarioEnum = TipoUsuarioEnum.CLIENTE

class UsuarioCreate(UsuarioBase):
    senha: str  # Senha em texto puro, que será hashada

class UsuarioResponse(UsuarioBase):
    id: int
    criado_em: str

    class Config:
        from_attributes = True
