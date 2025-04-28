from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.historico_pagamento import (
    HistoricoPagamentoCreate,
    HistoricoPagamentoResponse
)
from app.services import historico_pagamento as crud
from app.core.security import get_current_user  # Função de autenticação para segurança

router = APIRouter()


# 🧾 Criar novo histórico de pagamento
@router.post(
    "/",
    response_model=HistoricoPagamentoResponse,
    summary="Criar histórico de pagamento",
    status_code=status.HTTP_201_CREATED,
    response_description="Histórico de pagamento criado com sucesso"
)
def criar_historico_pagamento(
        dados: HistoricoPagamentoCreate,
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Cria um novo histórico de pagamento com base nas informações fornecidas.

    **Parâmetros**:
        - **dados**: Informações do pagamento que serão registradas no histórico.

    **Respostas**:
        - **201 Created**: Histórico de pagamento criado com sucesso.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    return crud.criar_historico_pagamento(db, dados)


# 📜 Listar todos os históricos de pagamento
@router.get(
    "/",
    response_model=List[HistoricoPagamentoResponse],
    summary="Listar históricos de pagamento",
    response_description="Lista de históricos de pagamento"
)
def listar_historicos_pagamento(
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Lista todos os históricos de pagamento registrados no sistema.

    **Respostas**:
        - **200 OK**: Retorna a lista de históricos de pagamento.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    return crud.listar_historicos(db)


# 🔍 Buscar históricos por ID de pagamento
@router.get(
    "/por-pagamento/{pagamento_id}",
    response_model=List[HistoricoPagamentoResponse],
    summary="Buscar históricos por pagamento",
    response_description="Lista de históricos de pagamento por ID de pagamento"
)
def buscar_historico_por_pagamento(
        pagamento_id: int,
        db: Session = Depends(get_db),
        usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Busca os históricos de pagamento relacionados a um ID de pagamento específico.

    **Parâmetros**:
        - **pagamento_id**: ID do pagamento para o qual queremos buscar os históricos.

    **Respostas**:
        - **200 OK**: Retorna a lista com os históricos encontrados para o pagamento solicitado.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
        - **404 Not Found**: Se nenhum histórico de pagamento for encontrado para o ID fornecido.
    """
    return crud.buscar_por_pagamento(db, pagamento_id)
