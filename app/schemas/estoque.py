from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

class EstoqueCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(..., ge=0)  # Garante que não seja negativo


class EstoqueResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True  # ✅ Necessário para conversão do SQLAlchemy para Pydantic


class EstoqueUpdate(BaseModel):
    quantidade: int = Field(..., ge=0)  # Atualiza a quantidade e impede valores negativos
