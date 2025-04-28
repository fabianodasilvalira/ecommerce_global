from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.core.security import get_current_user  # Função de autenticação
from app.db.database import get_db
from app.models import Usuario
from app.services.lista_desejos_service import ListaDesejosService
from app.schemas.lista_desejos_schema import (
    ListaDesejosCreate,
    ListaDesejosResponse,
)

router = APIRouter()

# 📌 Adicionar produto à lista de desejos (Protegido)
@router.post(
    "/",
    response_model=ListaDesejosResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar produto à lista de desejos",
)
def adicionar_produto_lista(
    dados: ListaDesejosCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)  # Obtém o usuário autenticado
):
    """
    Adiciona um produto à lista de desejos do usuário autenticado.

    **Protegido**: Apenas usuários autenticados podem adicionar produtos à sua lista de desejos.

    - **Parâmetros**:
        - **dados**: Detalhes do produto a ser adicionado.
    - **Resposta**:
        - Produto adicionado à lista de desejos.
    """
    service = ListaDesejosService(db)
    return service.adicionar_produto(usuario.id, dados)

# 🔍 Listar produtos da lista de desejos (Protegido)
@router.get(
    "/",
    response_model=List[ListaDesejosResponse],
    summary="Listar produtos da lista de desejos",
)
def listar_lista_desejos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)  # Obtém o usuário autenticado
):
    """
    Lista todos os produtos na lista de desejos do usuário autenticado.

    **Protegido**: Apenas usuários autenticados podem acessar sua lista de desejos.

    - **Resposta**:
        - Lista de produtos na lista de desejos do usuário.
    """
    service = ListaDesejosService(db)
    return service.listar_desejos_usuario(usuario.id)

# 🗑️ Remover produto da lista de desejos (Protegido)
@router.delete(
    "/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover produto da lista de desejos",
)
def remover_produto_lista(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)  # Obtém o usuário autenticado
):
    """
    Remove um produto da lista de desejos do usuário autenticado.

    **Protegido**: Apenas usuários autenticados podem remover produtos de sua lista de desejos.

    - **Parâmetros**:
        - **produto_id**: ID do produto a ser removido.
    """
    service = ListaDesejosService(db)
    service.remover_produto(usuario.id, produto_id)
