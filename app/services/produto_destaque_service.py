from typing import List

from sqlalchemy.orm import Session, joinedload

from app.models import ProdutoDestaque
from app.schemas.produto_destaque_schema import ProdutoDestaqueCreate, ProdutoDestaqueResponse


def listar_destaques(db: Session) -> List[ProdutoDestaqueResponse]:
    destaques = db.query(ProdutoDestaque).options(joinedload(ProdutoDestaque.produto)).all()
    return [ProdutoDestaqueResponse.model_validate(d) for d in destaques]

def criar_destaque(db: Session, dados: ProdutoDestaqueCreate):
    destaque = ProdutoDestaque(produto_id=dados.produto_id)
    db.add(destaque)
    db.commit()
    db.refresh(destaque)
    return destaque

def remover_destaque(db: Session, id: int):
    destaque = db.query(ProdutoDestaque).filter(ProdutoDestaque.id == id).first()
    if destaque:
        db.delete(destaque)
        db.commit()
        return True
    return False
