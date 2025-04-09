from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.produto_destaque_schema import ProdutoDestaqueCreate, ProdutoDestaqueResponse
from app.services import produto_destaque_service

router = APIRouter()

@router.get("/", response_model=List[ProdutoDestaqueResponse])
def listar(db: Session = Depends(get_db)):
    return produto_destaque_service.listar_destaques(db)

@router.post("/", response_model=ProdutoDestaqueResponse)
def criar(dados: ProdutoDestaqueCreate, db: Session = Depends(get_db)):
    return produto_destaque_service.criar_destaque(db, dados)

@router.delete("/{id}", status_code=204)
def deletar(id: int, db: Session = Depends(get_db)):
    sucesso = produto_destaque_service.remover_destaque(db, id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Destaque não encontrado")
