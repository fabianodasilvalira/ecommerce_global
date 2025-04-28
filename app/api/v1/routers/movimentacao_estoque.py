from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.movimentacao_estoque import MovimentacaoEstoqueOut, MovimentacaoEstoqueCreate
from app.services import movimentacao_estoque as service
from app.services.auth import obter_usuario_logado
from app.models.usuario import TipoUsuarioEnum, Usuario

router = APIRouter()


# 📌 Criar uma movimentação de estoque (Protegido por ADMIN)
@router.post("/", response_model=MovimentacaoEstoqueOut, status_code=status.HTTP_201_CREATED)
async def criar_movimentacao(
        movimentacao: MovimentacaoEstoqueCreate,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Cria uma nova movimentação de estoque.

    **Protegido**: Apenas administradores podem criar movimentações de estoque.

    - **Parâmetros**:
        - **movimentacao**: Dados da movimentação de estoque a ser criada.
    - **Resposta**:
        - Dados da movimentação de estoque recém-criada.
    """
    if usuario_logado.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas administradores podem criar movimentações de estoque.")

    return service.criar_movimentacao_estoque(db, movimentacao)


# 🔍 Listar movimentações de estoque (Público ou Protegido)
@router.get("/", response_model=List[MovimentacaoEstoqueOut])
async def listar_movimentacoes(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Lista todas as movimentações de estoque.

    **Público**: Qualquer usuário pode listar movimentações de estoque, mas a quantidade de itens retornados pode ser limitada.

    - **Parâmetros**:
        - **skip**: Número de registros a serem pulados (usado para paginação).
        - **limit**: Número de registros a serem retornados (usado para limitar o tamanho da resposta).
    - **Resposta**:
        - Lista de movimentações de estoque.
    """
    return service.listar_movimentacoes(db, skip=skip, limit=limit)
