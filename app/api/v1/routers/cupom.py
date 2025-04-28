from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Cupom
from app.schemas.cupom_schema import CupomCreate, CupomResponse, CupomUpdate
from app.services.cupom_service import criar_cupom, listar_cupons, buscar_cupom_por_codigo, desativar_cupom, \
    atualizar_cupom_por_id, atualizar_cupom_por_codigo
from app.core.security import get_current_user  # Função para autenticar usuário

router = APIRouter()

# 🧾 Adicionar um novo cupom
@router.post(
    "/",
    response_model=CupomResponse,
    summary="Criar um novo cupom",
    status_code=status.HTTP_201_CREATED,
    response_description="Cupom criado com sucesso"
)
def adicionar_cupom(
    cupom_data: CupomCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Adiciona um novo cupom ao sistema.

    **Parâmetros**:
        - **cupom_data**: Dados do cupom a ser criado.

    **Respostas**:
        - **201 Created**: Retorna o cupom criado com sucesso.
        - **400 Bad Request**: Caso o código do cupom já exista.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    if buscar_cupom_por_codigo(db, cupom_data.codigo):
        raise HTTPException(status_code=400, detail="Código de cupom já existe")

    return criar_cupom(db, cupom_data)


# ✅ Atualizar cupom por ID
@router.put(
    "/{cupom_id}",
    response_model=CupomResponse,
    summary="Atualizar cupom por ID",
    response_description="Cupom atualizado com sucesso"
)
def editar_cupom_por_id(
    cupom_id: int,
    cupom_data: CupomUpdate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Atualiza as informações de um cupom existente usando seu ID.

    **Parâmetros**:
        - **cupom_id**: ID do cupom a ser atualizado.
        - **cupom_data**: Dados do cupom atualizados.

    **Respostas**:
        - **200 OK**: Retorna o cupom atualizado.
        - **404 Not Found**: Caso o cupom com o ID fornecido não exista.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    cupom = atualizar_cupom_por_id(db, cupom_id, cupom_data)
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return cupom


# ✅ Atualizar cupom por Código
@router.put(
    "/codigo/{codigo}",
    response_model=CupomResponse,
    summary="Atualizar cupom por código",
    response_description="Cupom atualizado com sucesso"
)
def editar_cupom_por_codigo(
    codigo: str,
    cupom_data: CupomUpdate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Atualiza as informações de um cupom existente usando seu código.

    **Parâmetros**:
        - **codigo**: Código do cupom a ser atualizado.
        - **cupom_data**: Dados atualizados do cupom.

    **Respostas**:
        - **200 OK**: Retorna o cupom atualizado.
        - **404 Not Found**: Caso o cupom com o código fornecido não exista.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    cupom = atualizar_cupom_por_codigo(db, codigo, cupom_data)
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return cupom


# 📜 Listar todos os cupons
@router.get(
    "/",
    response_model=list[CupomResponse],
    summary="Listar todos os cupons",
    response_description="Lista de cupons cadastrados"
)
def listar_todos_cupons(db: Session = Depends(get_db), usuario: str = Depends(get_current_user)):
    """
    Retorna todos os cupons cadastrados no sistema.

    **Respostas**:
        - **200 OK**: Retorna a lista de cupons.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    return listar_cupons(db)


# 🔍 Buscar cupom pelo código
@router.get(
    "/{codigo}",
    response_model=CupomResponse,
    summary="Buscar cupom por código",
    response_description="Detalhes do cupom encontrado"
)
def buscar_cupom(
    codigo: str,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Busca um cupom específico utilizando seu código.

    **Parâmetros**:
        - **codigo**: Código do cupom a ser buscado.

    **Respostas**:
        - **200 OK**: Retorna os detalhes do cupom.
        - **404 Not Found**: Caso o cupom com o código fornecido não exista.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    cupom = buscar_cupom_por_codigo(db, codigo)
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return cupom


# 🗑️ Desativar cupom por ID
@router.put(
    "/{cupom_id}/desativar",
    response_model=CupomResponse,
    summary="Desativar cupom",
    response_description="Cupom desativado com sucesso"
)
def desativar_cupom_por_id(
    cupom_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # Acesso do usuário autenticado
):
    """
    Desativa um cupom específico no sistema.

    **Parâmetros**:
        - **cupom_id**: ID do cupom a ser desativado.

    **Respostas**:
        - **200 OK**: Retorna o cupom desativado com sucesso.
        - **404 Not Found**: Caso o cupom com o ID fornecido não exista.
        - **401 Unauthorized**: Se o usuário não estiver autenticado.
    """
    cupom = desativar_cupom(db, cupom_id)
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return cupom
