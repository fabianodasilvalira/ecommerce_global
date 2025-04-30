from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.database import Base


class ItemCarrinho(Base):
    __tablename__ = "item_carrinho"

    id = Column(Integer, primary_key=True, index=True)
    carrinho_id = Column(Integer, ForeignKey("carrinho.id", ondelete="CASCADE"))
    produto_id = Column(Integer, ForeignKey("produto.id"))
    quantidade = Column(Integer, default=1)
    valor_unitario = Column(Numeric(10, 2))
    valor_total = Column(Numeric(10, 2))

    # Alterado: Adicionei cascade para evitar problemas de deleção
    carrinho = relationship("Carrinho", back_populates="itens")
    produto = relationship("Produto", lazy="joined")  # Alterado para eager loading

    def __init__(self, produto_id, quantidade=1, **kwargs):
        super().__init__(**kwargs)
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.valor_unitario = self.produto.preco_final  # Preço base do produto
        self.calcular_total()

    def calcular_total(self):
        if self.valor_unitario and self.quantidade:
            self.valor_total = self.valor_unitario * self.quantidade
        else:
            self.valor_total = Decimal("0.00")