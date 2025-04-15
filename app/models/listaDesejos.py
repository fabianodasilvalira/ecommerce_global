from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base


class ListaDesejos(Base):
    __tablename__ = "lista_desejos"
    __table_args__ = (
        UniqueConstraint("usuario_id", "produto_id", name="uix_usuario_produto"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, index=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produto.id", ondelete="CASCADE"), nullable=False, index=True)
    criado_em: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="lista_desejos")
    produto: Mapped["Produto"] = relationship("Produto")
