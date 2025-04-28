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
from app.core.security import get_current_user  # Função para autenticar usuário

router = APIRouter()

# 🖼️ Adicionar imagem à categoria
@router.post(
    "/",
    response_model=CategoriaImagemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar imagem à categoria",
    response_description="Imagem adicionada com sucesso"
)
async def criar_imagem_endpoint(
    imagem: CategoriaImagemCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Adiciona uma nova imagem à categoria especificada.

    **Parâmetros**:
        - **imagem**: Dados da imagem a ser criada.

    **Respostas**:
        - **201 Created**: Retorna a imagem adicionada com sucesso.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    return criar_categoria_imagem(db, imagem)


# 🖼️ Listar imagens de uma categoria
@router.get(
    "/categoria/{categoria_id}",
    response_model=List[CategoriaImagemResponse],
    summary="Listar imagens da categoria ordenadas",
    response_description="Lista de imagens da categoria"
)
async def listar_imagens_endpoint(
    categoria_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Retorna uma lista de imagens ordenadas para uma categoria específica.

    **Parâmetros**:
        - **categoria_id**: ID da categoria para listar as imagens.

    **Respostas**:
        - **200 OK**: Retorna a lista de imagens da categoria.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    return listar_imagens_por_categoria(db, categoria_id)


# 🖼️ Buscar imagem por ID
@router.get(
    "/{imagem_id}",
    response_model=CategoriaImagemResponse,
    summary="Buscar imagem por ID",
    response_description="Detalhes da imagem encontrada"
)
async def buscar_imagem_endpoint(
    imagem_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Busca uma imagem específica usando seu ID.

    **Parâmetros**:
        - **imagem_id**: ID da imagem a ser buscada.

    **Respostas**:
        - **200 OK**: Retorna os detalhes da imagem.
        - **404 Not Found**: Caso a imagem com o ID fornecido não exista.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    imagem = buscar_imagem(db, imagem_id)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return imagem


# 🗑️ Deletar imagem por ID
@router.delete(
    "/{imagem_id}",
    response_model=CategoriaImagemResponse,
    summary="Deletar imagem",
    response_description="Imagem deletada com sucesso"
)
async def deletar_imagem_endpoint(
    imagem_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Deleta uma imagem específica do sistema.

    **Parâmetros**:
        - **imagem_id**: ID da imagem a ser deletada.

    **Respostas**:
        - **200 OK**: Retorna a imagem deletada com sucesso.
        - **404 Not Found**: Caso a imagem com o ID fornecido não exista.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    imagem = deletar_imagem(db, imagem_id)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return imagem


# 🔄 Reordenar imagens de uma categoria
@router.put(
    "/reordenar",
    status_code=status.HTTP_200_OK,
    summary="Reordenar imagens de uma categoria",
    description="Recebe uma lista com IDs e novas ordens para reordenar imagens da categoria.",
    response_description="Imagens reordenadas com sucesso"
)
async def reordenar_imagens_endpoint(
    ordens: List[CategoriaImagemReorder] = Body(..., description="Lista com ID e nova ordem"),
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Reordena as imagens dentro de uma categoria conforme a nova ordem recebida.

    **Parâmetros**:
        - **ordens**: Lista com os IDs das imagens e as novas ordens.

    **Respostas**:
        - **200 OK**: Confirmação de que as imagens foram reordenadas com sucesso.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    reordenar_imagens(db, ordens)
    return {"msg": "Imagens reordenadas com sucesso"}
