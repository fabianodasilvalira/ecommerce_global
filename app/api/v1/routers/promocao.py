from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.promocao_service import (
    criar_promocao_service,
    listar_promocoes_ativas_service,
    buscar_promocao_service,
    editar_promocao_service,
    inativar_promocao_service
)
from app.schemas.promocao_schema import PromocaoCreate, PromocaoResponse, PromocaoUpdate
from app.services.auth import obter_usuario_logado
from app.models.usuario import TipoUsuarioEnum, Usuario

router = APIRouter()


# 📌 Criar promoção (Protegido)
@router.post("/", response_model=PromocaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_promocao(
        promocao: PromocaoCreate,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Cria uma nova promoção.

    **Protegido**: Apenas administradores podem criar promoções.

    - **Parâmetros**:
        - **promocao**: Objeto com os dados da promoção a ser criada.
    - **Resposta**:
        - Retorna os dados da promoção recém-criada.
    """
    if usuario_logado.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas administradores podem criar promoções.")

    try:
        return criar_promocao_service(db, promocao)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 🔍 Listar promoções ativas (Público ou Protegido)
@router.get("/", response_model=List[PromocaoResponse])
async def listar_promocoes_ativas(
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Lista as promoções ativas no sistema.

    **Público**: Usuários podem ver as promoções ativas.

    - **Resposta**:
        - Lista de promoções ativas.
    """
    return listar_promocoes_ativas_service(db)


# 🔍 Buscar promoção por ID (Público ou Protegido)
@router.get("/{promocao_id}", response_model=PromocaoResponse)
async def buscar_promocao(
        promocao_id: int,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Busca uma promoção específica pelo ID.

    **Público**: Usuários podem buscar promoções ativas pelo ID.

    - **Parâmetros**:
        - **promocao_id**: ID da promoção a ser buscada.
    - **Resposta**:
        - Dados da promoção encontrada.
    """
    return buscar_promocao_service(db, promocao_id)


# ✏️ Editar promoção (Protegido)
@router.put("/{promocao_id}/editar", response_model=PromocaoResponse)
async def editar_promocao(
        promocao_id: int,
        update_data: PromocaoUpdate,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Edita os dados de uma promoção existente.

    **Protegido**: Apenas administradores podem editar promoções.

    - **Parâmetros**:
        - **promocao_id**: ID da promoção a ser editada.
        - **update_data**: Dados para atualização da promoção.
    - **Resposta**:
        - Dados da promoção editada.
    """
    if usuario_logado.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas administradores podem editar promoções.")

    try:
        return editar_promocao_service(db, promocao_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 🚫 Inativar promoção (Protegido)
@router.put("/{promocao_id}/inativar", response_model=PromocaoResponse)
async def inativar_promocao(
        promocao_id: int,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Inativa uma promoção específica.

    **Protegido**: Apenas administradores podem inativar promoções.

    - **Parâmetros**:
        - **promocao_id**: ID da promoção a ser inativada.
    - **Resposta**:
        - Dados da promoção inativada.
    """
    if usuario_logado.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas administradores podem inativar promoções.")

    try:
        return inativar_promocao_service(db, promocao_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
