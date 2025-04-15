from fastapi import APIRouter, Depends, status
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

@router.post(
    "/",
    response_model=ListaDesejosResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Adicionar à lista de desejos"
)
def adicionar_produto_lista(
    dados: ListaDesejosCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)  # Obtém o usuário autenticado
):
    # O `usuario.id` agora contém o ID do usuário autenticado
    service = ListaDesejosService(db)
    return service.adicionar_produto(usuario.id, dados)


@router.get(
    "/",
    response_model=List[ListaDesejosResponse],
    summary="Listar produtos da lista de desejos"
)
def listar_lista_desejos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)  # Obtém o usuário autenticado
):
    # O `usuario.id` agora contém o ID do usuário autenticado
    service = ListaDesejosService(db)
    return service.listar_desejos_usuario(usuario.id)




@router.delete(
    "/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover produto da lista de desejos"
)
def remover_produto_lista(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)  # Obtém o usuário autenticado
):
    # O `usuario.id` agora contém o ID do usuário autenticado
    service = ListaDesejosService(db)
    service.remover_produto(usuario.id, produto_id)
