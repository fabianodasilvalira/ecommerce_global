from sqlalchemy.orm import Session
from app.models import ProdutoDestaque
from app.schemas.produto_destaque_schema import ProdutoDestaqueCreate, ProdutoDestaqueUpdate
from datetime import datetime


class ProdutoDestaqueService:
    def __init__(self, db: Session):
        self.db = db

    def criar_destaque(self, destaque: ProdutoDestaqueCreate):
        db_destaque = ProdutoDestaque(
            produto_id=destaque.produto_id,
            posicao=destaque.posicao,
            tipo_destaque=destaque.tipo_destaque
        )
        self.db.add(db_destaque)
        self.db.commit()
        self.db.refresh(db_destaque)
        return db_destaque

    def listar_destaques(self, tipo: str = None, ativo: bool = True):
        query = self.db.query(ProdutoDestaque)

        if tipo:
            query = query.filter(ProdutoDestaque.tipo_destaque == tipo)

        if ativo is not None:
            query = query.filter(ProdutoDestaque.ativo == ativo)

        return query.order_by(ProdutoDestaque.posicao).all()

    def obter_destaque_por_id(self, destaque_id: int):
        return self.db.query(ProdutoDestaque).filter(ProdutoDestaque.id == destaque_id).first()

    def atualizar_destaque(self, destaque_id: int, destaque: ProdutoDestaqueUpdate):
        db_destaque = self.obter_destaque_por_id(destaque_id)
        if not db_destaque:
            return None

        update_data = destaque.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_destaque, key, value)

        self.db.commit()
        self.db.refresh(db_destaque)
        return db_destaque

    def remover_destaque(self, destaque_id: int):
        db_destaque = self.obter_destaque_por_id(destaque_id)
        if db_destaque:
            self.db.delete(db_destaque)
            self.db.commit()
        return db_destaque

    def alternar_status_destaque(self, destaque_id: int):
        db_destaque = self.obter_destaque_por_id(destaque_id)
        if db_destaque:
            db_destaque.ativo = not db_destaque.ativo
            self.db.commit()
            self.db.refresh(db_destaque)
        return db_destaque