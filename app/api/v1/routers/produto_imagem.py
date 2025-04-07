from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.produto_imagem import ProdutoImagemCreate, ProdutoImagemResponse
from app.services import produto_imagem_service as service

router = APIRouter()


@router.post("/", response_model=ProdutoImagemResponse)
def adicionar_imagem(imagem: ProdutoImagemCreate, db: Session = Depends(get_db)):
    return service.adicionar_imagem(db, imagem)


@router.get("/{produto_id}", response_model=list[ProdutoImagemResponse])
def listar_imagens(produto_id: int, db: Session = Depends(get_db)):
    return service.listar_imagens(db, produto_id)


@router.delete("/{imagem_id}", status_code=204)
def remover_imagem(imagem_id: int, db: Session = Depends(get_db)):
    if not service.remover_imagem(db, imagem_id):
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
