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
from app.core.security import get_current_user  # Função para autenticar usuário

router = APIRouter()

# 🏷️ Criar uma nova categoria
@router.post(
    "/",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma nova categoria",
    description="Cria uma nova categoria com os dados fornecidos.",
    response_description="Categoria criada com sucesso"
)
async def criar_categoria_endpoint(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Cria uma nova categoria no banco de dados.

    **Parâmetros**:
        - **nome**: Nome da categoria (único)
        - **slug**: Slug para URL amigável
        - **descricao**, **cor_destaque**, etc.: Campos opcionais

    **Respostas**:
        - **201 Created**: Categoria criada com sucesso.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    return criar_categoria(db, categoria)


# 📋 Listar categorias
@router.get(
    "/",
    response_model=List[CategoriaResponse],
    summary="Listar categorias",
    description="Lista todas as categorias cadastradas, com opção de incluir inativas.",
    response_description="Lista de categorias"
)
async def listar_categorias_endpoint(
    incluir_inativas: bool = Query(False, description="Incluir categorias inativas"),
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Retorna todas as categorias ativas (ou todas, se incluir_inativas=True).

    **Parâmetros**:
        - **incluir_inativas**: Se True, inclui categorias inativas.

    **Respostas**:
        - **200 OK**: Lista de categorias.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    return listar_categorias(db, incluir_inativas)


# 🔍 Buscar categoria por ID
@router.get(
    "/{categoria_id}",
    response_model=CategoriaResponse,
    summary="Buscar categoria por ID",
    responses={404: {"description": "Categoria não encontrada"}},
    description="Retorna os detalhes de uma categoria específica pelo ID.",
    response_description="Detalhes da categoria"
)
async def buscar_categoria_endpoint(
    categoria_id: int = Path(..., description="ID da categoria"),
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Busca uma categoria pelo ID informado.

    **Parâmetros**:
        - **categoria_id**: ID da categoria a ser buscada.

    **Respostas**:
        - **200 OK**: Detalhes da categoria.
        - **404 Not Found**: Caso a categoria com o ID fornecido não exista.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    categoria = buscar_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria


# ✏️ Atualizar categoria
@router.put(
    "/{categoria_id}",
    response_model=CategoriaResponse,
    summary="Atualizar categoria",
    responses={404: {"description": "Categoria não encontrada"}},
    description="Atualiza os dados de uma categoria existente.",
    response_description="Categoria atualizada com sucesso"
)
async def atualizar_categoria_endpoint(
    categoria_id: int = Path(..., description="ID da categoria a ser atualizada"),
    categoria_dados: CategoriaUpdate = ...,  # Requer o corpo com dados
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Atualiza os campos da categoria com base nos dados fornecidos.

    **Parâmetros**:
        - **categoria_id**: ID da categoria a ser atualizada.
        - **categoria_dados**: Dados para atualizar a categoria.

    **Respostas**:
        - **200 OK**: Categoria atualizada com sucesso.
        - **404 Not Found**: Caso a categoria com o ID fornecido não exista.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    categoria = atualizar_categoria(db, categoria_id, categoria_dados)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria


# 🚫 Inativar categoria
@router.delete(
    "/{categoria_id}",
    response_model=CategoriaResponse,
    summary="Inativar categoria",
    responses={404: {"description": "Categoria não encontrada"}},
    description="""Inativa uma categoria e todos os produtos relacionados a ela. A categoria continua registrada para fins históricos.""",
    response_description="Categoria inativada com sucesso"
)
async def inativar_categoria_endpoint(
    categoria_id: int = Path(..., description="ID da categoria a ser inativada"),
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Marca uma categoria como inativa e atualiza os produtos relacionados.

    **Parâmetros**:
        - **categoria_id**: ID da categoria a ser inativada.

    **Respostas**:
        - **200 OK**: Categoria inativada com sucesso.
        - **404 Not Found**: Caso a categoria com o ID fornecido não exista.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    categoria = inativar_categoria_e_atualizar_produtos(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria
