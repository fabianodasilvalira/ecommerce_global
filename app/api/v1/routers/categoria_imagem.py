from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.categoria_imagem_schema import (
    CategoriaImagemCreate,
    CategoriaImagemResponse,
    CategoriaImagemReorder
)
from app.services.categoria_imagem_service import (
    criar_categoria_imagem,
    listar_imagens_por_categoria,
    buscar_imagem,
    deletar_imagem,
    reordenar_imagens
)

router = APIRouter()

@router.post(
    "/",
    response_model=CategoriaImagemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar imagem à categoria"
)
async def criar_imagem_endpoint(
    imagem: CategoriaImagemCreate,
    db: Session = Depends(get_db)
):
    return criar_categoria_imagem(db, imagem)

@router.get(
    "/categoria/{categoria_id}",
    response_model=List[CategoriaImagemResponse],
    summary="Listar imagens da categoria ordenadas"
)
async def listar_imagens_endpoint(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    return listar_imagens_por_categoria(db, categoria_id)

@router.get(
    "/{imagem_id}",
    response_model=CategoriaImagemResponse,
    summary="Buscar imagem por ID"
)
async def buscar_imagem_endpoint(
    imagem_id: int,
    db: Session = Depends(get_db)
):
    imagem = buscar_imagem(db, imagem_id)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return imagem

@router.delete(
    "/{imagem_id}",
    response_model=CategoriaImagemResponse,
    summary="Deletar imagem"
)
async def deletar_imagem_endpoint(
    imagem_id: int,
    db: Session = Depends(get_db)
):
    imagem = deletar_imagem(db, imagem_id)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return imagem

@router.put(
    "/reordenar",
    status_code=status.HTTP_200_OK,
    summary="Reordenar imagens de uma categoria",
    description="Recebe uma lista com IDs e novas ordens para reordenar imagens da categoria."
)
async def reordenar_imagens_endpoint(
    ordens: List[CategoriaImagemReorder] = Body(..., description="Lista com ID e nova ordem"),
    db: Session = Depends(get_db)
):
    reordenar_imagens(db, ordens)
    return {"msg": "Imagens reordenadas com sucesso"}
