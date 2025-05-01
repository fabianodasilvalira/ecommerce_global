from _pydecimal import Decimal
from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models import Produto


class ItemCarrinho(Base):
    __tablename__ = "item_carrinho"

    id = Column(Integer, primary_key=True, index=True)
    carrinho_id = Column(Integer, ForeignKey("carrinho.id", ondelete="CASCADE"))
    produto_id = Column(Integer, ForeignKey("produto.id"))
    quantidade = Column(Integer, default=1)
    valor_unitario = Column(Numeric(10, 2))
    valor_total = Column(Numeric(10, 2))

    carrinho = relationship("Carrinho", back_populates="itens")
    produto = relationship("Produto", lazy="joined")

    def __init__(self, produto_id, quantidade=1, produto=None, **kwargs):
        super().__init__(**kwargs)
        self.produto_id = produto_id
        self.quantidade = quantidade

        # Se o produto foi passado diretamente (por exemplo, de uma camada externa), usamos esse valor
        if produto:
            self.produto = produto
        else:
            # Caso contrário, consulte o banco para o produto
            self.produto = Produto.query.filter(Produto.id == self.produto_id).first()

        if self.produto:
            self.valor_unitario = self.produto.preco_final
        else:
            self.valor_unitario = Decimal("0.00")

        self.calcular_total()

    def calcular_total(self):
        if self.valor_unitario and self.quantidade:
            self.valor_total = self.valor_unitario * self.quantidade
        else:
            self.valor_total = Decimal("0.00")
