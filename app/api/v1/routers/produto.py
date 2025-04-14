from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.produto_service import (
    criar_produto,
    listar_produtos_service,
    buscar_produto_service,
    atualizar_produto_service,
    inativar_produto_service
)
from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse, ProdutoUpdate

router = APIRouter()

# Criar um novo produto
@router.post("/", response_model=ProdutoResponse)
def criar_novo_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    return criar_produto(db, produto)

# Listar todos os produtos ativos
@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return listar_produtos_service(db)

# Buscar um produto por ID
@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    return buscar_produto_service(db, produto_id)

@router.get("/{produto_id}/completo", response_model=ProdutoResponse)
def buscar_produto_completo(produto_id: int, db: Session = Depends(get_db)):
    return buscar_produto_service(db, produto_id)

# Editar um produto
@router.put("/{produto_id}/editar", response_model=ProdutoResponse)
def editar_produto(produto_id: int, update_data: ProdutoUpdate, db: Session = Depends(get_db)):
    return atualizar_produto_service(db, produto_id, update_data.dict(exclude_unset=True))

# Inativar um produto
@router.put("/{produto_id}/inativar", response_model=ProdutoResponse)
def inativar_produto(produto_id: int, db: Session = Depends(get_db)):
    return inativar_produto_service(db, produto_id)
