from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.models.usuario import Usuario
from app.db.database import Base


class Carrinho(Base):
    __tablename__ = "carrinho"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
    is_finalizado = Column(Boolean, default=False)

    # Alterado: Adicionei cascade para evitar problemas de deleção
    venda = relationship("Venda", back_populates="carrinho", uselist=False, cascade="save-update")

    # Alterado: Adicionei order_by para itens
    usuario = relationship("Usuario", back_populates="carrinho")
    itens = relationship(
        "ItemCarrinho",
        back_populates="carrinho",
        cascade="all, delete-orphan",
        order_by="ItemCarrinho.id"
    )

    # Alterado: Adicionei método para calcular subtotal
    @property
    def subtotal(self) -> float:
        return sum(float(item.valor_total) for item in self.itens)