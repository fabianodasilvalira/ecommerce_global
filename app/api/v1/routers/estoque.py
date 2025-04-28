from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.estoque import EstoqueCreate, EstoqueUpdate, EstoqueResponse
from app.services.estoque_service import (
    adicionar_estoque,
    obter_estoque,
    listar_estoque,
    atualizar_estoque,
    deletar_estoque
)
from app.core.security import get_current_user  # Função de autenticação

router = APIRouter()


# 🧾 Adicionar item ao estoque
@router.post(
    "/",
    response_model=EstoqueResponse,
    summary="Adicionar item ao estoque",
    status_code=status.HTTP_201_CREATED,
    response_description="Item adicionado ao estoque com sucesso"
)
def adicionar_item_estoque(
        estoque_data: EstoqueCreate,
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Adiciona um novo item ao estoque com base nas informações fornecidas.

    **Parâmetros**:
        - **estoque_data**: Dados do item que serão adicionados ao estoque.

    **Respostas**:
        - **201 Created**: Item adicionado ao estoque com sucesso.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    return adicionar_estoque(db, estoque_data)


# 📜 Listar todos os itens do estoque
@router.get(
    "/",
    response_model=List[EstoqueResponse],
    summary="Listar itens do estoque",
    response_description="Lista de itens no estoque"
)
def listar_itens_estoque(
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Lista todos os itens no estoque.

    **Respostas**:
        - **200 OK**: Retorna a lista de itens no estoque.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    return listar_estoque(db)


# 🔍 Buscar item no estoque por ID de produto
@router.get(
    "/{produto_id}/produto/",
    response_model=EstoqueResponse,
    summary="Buscar item no estoque por ID de produto",
    response_description="Detalhes do item encontrado no estoque"
)
def buscar_estoque(
        produto_id: int,
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Busca um item específico no estoque baseado no ID do produto.

    **Parâmetros**:
        - **produto_id**: ID do produto para buscar no estoque.

    **Respostas**:
        - **200 OK**: Retorna os detalhes do item encontrado.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
        - **404 Not Found**: Se o item com o ID fornecido não for encontrado.
    """
    return obter_estoque(db, produto_id)


# ✏️ Editar item no estoque
@router.put(
    "/{produto_id}",
    response_model=EstoqueResponse,
    summary="Editar item no estoque",
    response_description="Item do estoque atualizado com sucesso"
)
def editar_estoque(
        produto_id: int,
        estoque_data: EstoqueUpdate,
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Edita um item específico no estoque baseado no ID do produto e nos novos dados fornecidos.

    **Parâmetros**:
        - **produto_id**: ID do produto a ser editado no estoque.
        - **estoque_data**: Dados atualizados do item no estoque.

    **Respostas**:
        - **200 OK**: Item do estoque atualizado com sucesso.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
        - **404 Not Found**: Se o item com o ID fornecido não for encontrado.
    """
    return atualizar_estoque(db, produto_id, estoque_data)


# 🗑️ Remover item do estoque
@router.delete(
    "/{produto_id}",
    summary="Remover item do estoque",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Item removido do estoque com sucesso"
)
def remover_item_estoque(
        produto_id: int,
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Remove um item específico do estoque baseado no ID do produto.

    **Parâmetros**:
        - **produto_id**: ID do produto a ser removido do estoque.

    **Respostas**:
        - **204 No Content**: Item removido do estoque com sucesso.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
        - **404 Not Found**: Se o item com o ID fornecido não for encontrado.
    """
    return deletar_estoque(db, produto_id)
