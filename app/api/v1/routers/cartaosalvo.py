from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.db.database import get_db
from app.schemas.cartaosalvo_schema import CartaoSalvoCreate, CartaoSalvoResponse
from app.services import cartaosalvo_service
from app.models.usuario import Usuario

router = APIRouter()

@router.post(
    "/",
    response_model=CartaoSalvoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Salvar novo cartão",
    description="Salva um novo cartão de crédito (apenas os últimos 4 dígitos, bandeira, validade e nome) para o usuário autenticado."
)
def criar_cartao(
    cartao: CartaoSalvoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    """
    Cria um novo cartão salvo para o usuário atual.

    - **nome_cartao**: Nome impresso no cartão
    - **bandeira_cartao**: Bandeira (ex: Visa, MasterCard)
    - **ultimos_digitos**: Últimos 4 dígitos do cartão
    - **validade**: Validade no formato MM/AAAA
    """
    return cartaosalvo_service.criar_cartao_salvo(db, usuario.id, cartao)


@router.get(
    "/",
    response_model=List[CartaoSalvoResponse],
    summary="Listar cartões salvos",
    description="Retorna todos os cartões salvos do usuário autenticado."
)
def listar_cartoes(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    """
    Lista todos os cartões de crédito salvos pelo usuário atual.
    """
    return cartaosalvo_service.listar_cartoes_usuario(db, usuario.id)


@router.delete(
    "/{cartao_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar cartão",
    description="Remove um cartão salvo pelo ID, desde que pertença ao usuário autenticado."
)
def deletar_cartao(
    cartao_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    """
    Remove um cartão salvo do usuário autenticado.

    - **cartao_id**: ID do cartão a ser removido
    """
    sucesso = cartaosalvo_service.deletar_cartao_salvo(db, cartao_id, usuario.id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
