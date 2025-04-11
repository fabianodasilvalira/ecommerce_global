from sqlalchemy.orm import Session
from app.models.movimentacao_estoque import MovimentacaoEstoque
from app.schemas.movimentacao_estoque import MovimentacaoEstoqueCreate

def criar_movimentacao_estoque(db: Session, movimentacao: MovimentacaoEstoqueCreate):
    db_mov = MovimentacaoEstoque(**movimentacao.dict())
    db.add(db_mov)
    db.commit()
    db.refresh(db_mov)
    return db_mov

def listar_movimentacoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MovimentacaoEstoque).offset(skip).limit(limit).all()
