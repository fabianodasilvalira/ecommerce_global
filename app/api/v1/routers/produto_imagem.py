from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.produto_imagem_schema import (
    ProdutoImagemCreate,
    ProdutoImagemResponse, ProdutoImagemUpdate
)
from app.services.produto_imagem_service import (
    criar_imagem_produto,
    listar_imagens_produto,
    buscar_imagem_produto,
    deletar_imagem_produto, editar_imagem_produto
)

router = APIRouter()

@router.post("/", response_model=ProdutoImagemResponse, status_code=status.HTTP_201_CREATED)
def criar_imagem(imagem: ProdutoImagemCreate, db: Session = Depends(get_db)):
    return criar_imagem_produto(db, imagem)

@router.put("/{imagem_id}")
def atualizar_imagem(imagem_id: int, imagem_data: ProdutoImagemUpdate, db: Session = Depends(get_db)):
    imagem = editar_imagem_produto(db, imagem_id, imagem_data)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return imagem


@router.get("/produto/{produto_id}", response_model=List[ProdutoImagemResponse])
def listar_imagens(produto_id: int, db: Session = Depends(get_db)):
    return listar_imagens_produto(db, produto_id)

@router.get("/{imagem_id}", response_model=ProdutoImagemResponse)
def buscar_imagem(imagem_id: int, db: Session = Depends(get_db)):
    imagem = buscar_imagem_produto(db, imagem_id)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return imagem

@router.delete("/{imagem_id}", response_model=ProdutoImagemResponse)
def deletar_imagem(imagem_id: int, db: Session = Depends(get_db)):
    imagem = deletar_imagem_produto(db, imagem_id)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return imagem