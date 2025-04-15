from datetime import datetime
from pydantic import BaseModel
from app.schemas.produto_schema import ProdutoResponse

class ListaDesejosResponse(BaseModel):
    id: int
    criado_em: datetime
    produto: ProdutoResponse  # Detalhes do produto na lista de desejos

    class Config:
        orm_mode = True  # Permite que a classe seja convertida de modelos SQLAlchemy para Pydantic


class ListaDesejosCreate(BaseModel):
    produto_id: int

    class Config:
        orm_mode = True