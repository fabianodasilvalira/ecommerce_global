from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.produto_destaque_schema import (
    ProdutoDestaqueCreate,
    ProdutoDestaqueResponse,
    ProdutoDestaqueUpdate,
    ProdutoDestaqueComProduto,
    TipoDestaqueEnum
)
from app.services.produto_destaque_service import ProdutoDestaqueService

router = APIRouter()

# 📌 Endpoint para criar um novo destaque de produto
@router.post(
    "/",
    response_model=ProdutoDestaqueResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo destaque",
    description="Cria um novo registro de produto em destaque"
)
async def criar_destaque(
        destaque: ProdutoDestaqueCreate,
        db: Session = Depends(get_db)
) -> ProdutoDestaqueResponse:
    """
    Cria um novo destaque para um produto.

    - **produto_id**: ID do produto a ser destacado (obrigatório)
    - **posicao**: Ordem de exibição (opcional, 1-99)
    - **tipo_destaque**: Tipo de destaque (opcional, padrão: 'principal')
    """
    service = ProdutoDestaqueService(db)
    return service.criar_destaque(destaque)


# 📌 Endpoint para listar os destaques com filtros opcionais
@router.get(
    "/",
    response_model=List[ProdutoDestaqueComProduto],
    summary="Listar destaques",
    description="Lista todos os produtos em destaque com filtros opcionais"
)
async def listar_destaques(
        tipo: Optional[TipoDestaqueEnum] = None,
        ativo: Optional[bool] = True,
        db: Session = Depends(get_db)
) -> List[ProdutoDestaqueComProduto]:
    """
    Lista os produtos em destaque com filtros opcionais:

    - **tipo**: Filtra por tipo de destaque
    - **ativo**: Filtra por status ativo/inativo (padrão: True)
    """
    service = ProdutoDestaqueService(db)
    return service.listar_destaques(tipo, ativo)


# 📌 Endpoint para obter os detalhes de um destaque específico
@router.get(
    "/{destaque_id}",
    response_model=ProdutoDestaqueComProduto,
    summary="Obter destaque por ID",
    description="Retorna os detalhes de um destaque específico"
)
async def obter_destaque(
        destaque_id: int,
        db: Session = Depends(get_db)
) -> ProdutoDestaqueComProduto:
    """
    Obtém os detalhes de um destaque pelo seu ID.
    """
    service = ProdutoDestaqueService(db)
    destaque = service.obter_destaque_por_id(destaque_id)
    if not destaque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destaque não encontrado"
        )
    return destaque


# 📌 Endpoint para atualizar um destaque existente
@router.put(
    "/{destaque_id}",
    response_model=ProdutoDestaqueResponse,
    summary="Atualizar destaque",
    description="Atualiza as informações de um destaque existente"
)
async def atualizar_destaque(
        destaque_id: int,
        destaque: ProdutoDestaqueUpdate,
        db: Session = Depends(get_db)
) -> ProdutoDestaqueResponse:
    """
    Atualiza um destaque existente.

    Parâmetros atualizáveis:
    - **posicao**: Nova posição de exibição
    - **ativo**: Novo status
    - **tipo_destaque**: Novo tipo de destaque
    """
    service = ProdutoDestaqueService(db)
    return service.atualizar_destaque(destaque_id, destaque)


# 📌 Endpoint para remover um destaque
@router.delete(
    "/{destaque_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover destaque",
    description="Remove um destaque permanentemente"
)
async def remover_destaque(
        destaque_id: int,
        db: Session = Depends(get_db)
):
    """
    Remove um destaque pelo seu ID.
    """
    service = ProdutoDestaqueService(db)
    service.remover_destaque(destaque_id)


# 📌 Endpoint para alternar o status de um destaque
@router.patch(
    "/{destaque_id}/alternar-status",
    response_model=ProdutoDestaqueResponse,
    summary="Alternar status",
    description="Alterna o status ativo/inativo de um destaque"
)
async def alternar_status_destaque(
        destaque_id: int,
        db: Session = Depends(get_db)
) -> ProdutoDestaqueResponse:
    """
    Alterna o status (ativo/inativo) de um destaque.
    """
    service = ProdutoDestaqueService(db)
    return service.alternar_status_destaque(destaque_id)
