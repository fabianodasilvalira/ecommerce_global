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
    inativar_categoria_e_atualizar_produtos
)

router = APIRouter()
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

# Atualizar Categoria
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

# Inativar Categoria e atualizar produtos relacionados
@router.put("/{categoria_id}/inativar", response_model=CategoriaResponse)
async def inativar_categoria_endpoint(categoria_id: int, db: Session = Depends(get_db)):
    categoria = inativar_categoria_e_atualizar_produtos(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

