from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.db.database import get_db
from app.schemas.venda_schema import VendaCreate, VendaResponse, VendaDetalhadaResponse, VendaOut
from app.services.venda_service import criar_venda, listar_vendas_usuario, detalhar_venda, cancelar_venda
from app.models.usuario import Usuario

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=VendaOut)
async def criar_venda_endpoint(
        venda_data: VendaCreate,
        db: Session = Depends(get_db),
        usuario: Usuario = Depends(get_current_user)
):
    """
    Cria uma nova venda para o usuário autenticado.

    **Requer autenticação**
    - Apenas usuários autenticados podem criar uma venda.

    - **Parâmetros:**
      - **venda_data**: Dados para criação da venda (requisição do corpo).
      - **usuario**: O usuário autenticado.

    - **Resposta**:
      - Retorna os detalhes da venda criada.
    """
    return criar_venda(db=db, venda_data=venda_data, usuario=usuario)


@router.get("/usuario", response_model=List[VendaResponse])
async def listar_vendas_usuario_endpoint(
        db: Session = Depends(get_db),
        usuario: Usuario = Depends(get_current_user)
):
    """
    Lista todas as vendas do usuário autenticado.

    **Requer autenticação**
    - Apenas usuários autenticados podem acessar suas vendas.

    - **Resposta**:
      - Lista de vendas do usuário.
    """
    return listar_vendas_usuario(db=db, usuario=usuario)


@router.get("/{venda_id}", response_model=VendaOut)
async def detalhar_venda_endpoint(
        venda_id: int,
        db: Session = Depends(get_db),
        usuario: Usuario = Depends(get_current_user)
):
    """
    Retorna os detalhes de uma venda específica do usuário autenticado.

    **Requer autenticação**
    - Apenas usuários autenticados podem acessar o detalhamento de suas vendas.

    - **Parâmetros:**
      - **venda_id**: ID da venda a ser detalhada.

    - **Resposta**:
      - Detalhes da venda específica.
    """
    return detalhar_venda(db, venda_id, usuario)


@router.delete("/{venda_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancelar_venda_endpoint(
        venda_id: int,
        db: Session = Depends(get_db),
        usuario: Usuario = Depends(get_current_user)
):
    """
    Cancela uma venda específica do usuário autenticado.

    **Requer autenticação**
    - Apenas usuários autenticados podem cancelar suas vendas.

    - **Parâmetros:**
      - **venda_id**: ID da venda a ser cancelada.

    - **Resposta**:
      - Retorna código 204 No Content, indicando que a venda foi cancelada.
    """
    cancelar_venda(db=db, venda_id=venda_id, usuario=usuario)
    return None
