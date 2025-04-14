from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate
)
from app.services.categoria_service import (
    criar_categoria,
    listar_categorias,
    buscar_categoria,
    atualizar_categoria,
    inativar_categoria_e_atualizar_produtos
)

router = APIRouter()


@router.post(
    "/",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma nova categoria",
    description="Cria uma nova categoria com os dados fornecidos."
)
async def criar_categoria_endpoint(
        categoria: CategoriaCreate,
        db: Session = Depends(get_db)
):
    """
    Cria uma nova categoria no banco de dados.

    - **nome**: Nome da categoria (único)
    - **slug**: Slug para URL amigável
    - **descricao**, **cor_destaque**, etc.: Campos opcionais
    """
    return criar_categoria(db, categoria)


@router.get(
    "/",
    response_model=List[CategoriaResponse],
    summary="Listar categorias",
    description="Lista todas as categorias cadastradas, com opção de incluir inativas."
)
async def listar_categorias_endpoint(
        incluir_inativas: bool = Query(False, description="Incluir categorias inativas"),
        db: Session = Depends(get_db)
):
    """
    Retorna todas as categorias ativas (ou todas, se incluir_inativas=True).
    """
    return listar_categorias(db, incluir_inativas)


@router.get(
    "/{categoria_id}",
    response_model=CategoriaResponse,
    summary="Buscar categoria por ID",
    responses={
        404: {"description": "Categoria não encontrada"}
    },
    description="Retorna os detalhes de uma categoria específica pelo ID."
)
async def buscar_categoria_endpoint(
        categoria_id: int = Path(..., description="ID da categoria"),
        db: Session = Depends(get_db)
):
    """
    Busca uma categoria pelo ID informado.
    """
    categoria = buscar_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria


@router.put(
    "/{categoria_id}",
    response_model=CategoriaResponse,
    summary="Atualizar categoria",
    responses={
        404: {"description": "Categoria não encontrada"}
    },
    description="Atualiza os dados de uma categoria existente."
)
async def atualizar_categoria_endpoint(
        categoria_id: int = Path(..., description="ID da categoria a ser atualizada"),
        categoria_dados: CategoriaUpdate = ...,  # Requer o corpo com dados
        db: Session = Depends(get_db),
):
    """
    Atualiza os campos da categoria com base nos dados fornecidos.
    """
    categoria = atualizar_categoria(db, categoria_id, categoria_dados)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria


@router.delete(
    "/{categoria_id}",
    response_model=CategoriaResponse,
    summary="Inativar categoria",
    responses={
        404: {"description": "Categoria não encontrada"}
    },
    description="""
    Inativa uma categoria e todos os produtos relacionados a ela. A categoria continua registrada para fins históricos.
    """
)
async def inativar_categoria_endpoint(
        categoria_id: int = Path(..., description="ID da categoria a ser inativada"),
        db: Session = Depends(get_db)
):
    """
    Marca uma categoria como inativa e atualiza os produtos relacionados.
    """
    categoria = inativar_categoria_e_atualizar_produtos(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria
