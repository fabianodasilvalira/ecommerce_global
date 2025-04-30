from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ItemCarrinhoBase(BaseModel):
    produto_id: int
    quantidade: int
    valor_unitario: Optional[Decimal] = None
    valor_total: Optional[Decimal] = None
    carrinho_id: Optional[int] = None  # Aqui você pode garantir que o carrinho_id também seja refletido
    carrinho: Optional["CarrinhoBase"] = None  # Definir a relação com o carrinho (se necessário)

    class Config:
        orm_mode = True  # Permite a conversão automática de SQLAlchemy para Pydantic

class ItemCarrinhoPydantic(BaseModel):
    produto_id: int
    quantidade: int
    valor_unitario: Optional[float] = None  # Pode ser opcional
    valor_total: Optional[float] = None  # Pode ser opcional, calculado depois

    # Método para calcular o total, se os campos necessários forem fornecidos
    def calcular_total(self):
        if self.valor_unitario is not None and self.quantidade is not None:
            self.valor_total = self.valor_unitario * self.quantidade

    class Config:
        orm_mode = True  # Para permitir conversão de objetos SQLAlchemy para Pydantic