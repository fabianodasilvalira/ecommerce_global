from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.produto_destaque import ProdutoDestaqueCreate, ProdutoDestaqueResponse
from app.services import produto_destaque_service as service

router = APIRouter()

@router.post("/", response_model=ProdutoDestaqueResponse)
def adicionar_destaque(destaque: ProdutoDestaqueCreate, db: Session = Depends(get_db)):
    return service.adicionar_produto_destaque(db, destaque)

@router.delete("/{produto_id}", status_code=204)
def remover_destaque(produto_id: int, db: Session = Depends(get_db)):
    if not service.remover_produto_destaque(db, produto_id):
        raise HTTPException(status_code=404, detail="Produto destaque não encontrado")

@router.get("/", response_model=list[ProdutoDestaqueResponse])
def listar_destaques(db: Session = Depends(get_db)):
    return service.listar_destaques(db)
