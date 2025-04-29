from pydantic import BaseModel, constr
from datetime import datetime

class CartaoSalvoBase(BaseModel):
    bandeira: str
    ultimos_digitos: constr(min_length=4, max_length=4)
    nome_impresso: str | None = None

class CartaoSalvoCreate(CartaoSalvoBase):
    token_cartao: str

class CartaoSalvoResponse(CartaoSalvoBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True
