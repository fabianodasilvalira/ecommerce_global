from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.categoria_schema import CategoriaCreate, CategoriaResponse, CategoriaUpdate
from app.services.categoria_service import (
    criar_categoria,
    listar_categorias,
    buscar_categoria,
    atualizar_categoria,
    deletar_categoria
)

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.post("/", response_model=CategoriaResponse)
async def criar_categoria_endpoint(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    return criar_categoria(db, categoria)

@router.get("/", response_model=List[CategoriaResponse])
async def listar_categorias_endpoint(db: Session = Depends(get_db)):
    return listar_categorias(db)

@router.get("/{categoria_id}", response_model=CategoriaResponse)
async def buscar_categoria_endpoint(categoria_id: int, db: Session = Depends(get_db)):
    categoria = buscar_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@router.put("/{categoria_id}", response_model=CategoriaResponse)
async def atualizar_categoria_endpoint(
    categoria_id: int,
    categoria_dados: CategoriaUpdate,
    db: Session = Depends(get_db),

):
    categoria = atualizar_categoria(db, categoria_id, categoria_dados)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@router.delete("/{categoria_id}", status_code=204)
async def deletar_categoria_endpoint(categoria_id: int, db: Session = Depends(get_db)):
    categoria = deletar_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return None  # Retorna um status 204 sem conteúdo
