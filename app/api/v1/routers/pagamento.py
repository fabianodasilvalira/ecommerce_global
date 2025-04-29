from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.services import pagamento_service
from app.schemas import pagamento_schema as pagamento_schema

router = APIRouter()

@router.post(
    "/",
    response_model=pagamento_schema.PagamentoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo pagamento",
    description="Cria um novo registro de pagamento no sistema com base nos dados fornecidos."
)
def criar_pagamento(pagamento: pagamento_schema.PagamentoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo pagamento.

    - **valor**: Valor do pagamento
    - **metodo_pagamento**: Método utilizado (ex: crédito, débito, pix)
    - **descricao**: Descrição opcional do pagamento
    """
    return pagamento_service.criar_pagamento(db, pagamento)


@router.get(
    "/",
    response_model=List[pagamento_schema.PagamentoResponse],
    summary="Listar todos os pagamentos",
    description="Retorna uma lista de todos os pagamentos registrados no sistema, com suporte a paginação."
)
def listar_pagamentos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista os pagamentos registrados.

    - **skip**: Número de registros a pular (útil para paginação)
    - **limit**: Número máximo de registros a retornar
    """
    return pagamento_service.listar_pagamentos(db, skip=skip, limit=limit)


@router.get(
    "/{pagamento_id}",
    response_model=pagamento_schema.PagamentoResponse,
    summary="Buscar pagamento por ID",
    description="Retorna os detalhes de um pagamento específico com base no ID fornecido."
)
def buscar_pagamento(
    pagamento_id: int,
    db: Session = Depends(get_db)
):
    """
    Busca um pagamento pelo ID.

    - **pagamento_id**: ID do pagamento a ser buscado
    """
    return pagamento_service.buscar_pagamento(db, pagamento_id)


@router.put(
    "/{pagamento_id}",
    response_model=pagamento_schema.PagamentoResponse,
    summary="Atualizar pagamento",
    description="Atualiza os dados de um pagamento existente com base no ID."
)
def atualizar_pagamento(
    pagamento_id: int,
    pagamento_update: pagamento_schema.PagamentoUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um pagamento existente.

    - **pagamento_id**: ID do pagamento a ser atualizado
    - **pagamento_update**: Dados novos a serem aplicados
    """
    return pagamento_service.atualizar_pagamento(db, pagamento_id, pagamento_update)


@router.delete(
    "/{pagamento_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir pagamento",
    description="Remove um pagamento do sistema com base no ID fornecido."
)
def deletar_pagamento(
    pagamento_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um pagamento do sistema.

    - **pagamento_id**: ID do pagamento a ser excluído
    """
    pagamento_service.deletar_pagamento(db, pagamento_id)
    return {"detail": "Pagamento excluído com sucesso"}
