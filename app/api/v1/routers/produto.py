from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.produto_service import (
    criar_produto,
    listar_produtos_service,
    buscar_produto_service,
    atualizar_produto_service,
    inativar_produto_service
)
from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.services.auth import obter_usuario_logado
from app.models.usuario import TipoUsuarioEnum, Usuario

router = APIRouter()


# 📌 Criar um novo produto (Protegido por ADMIN)
@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar_novo_produto(
        produto: ProdutoCreate,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Cria um novo produto no sistema.

    **Protegido**: Apenas administradores podem criar novos produtos.

    - **Parâmetros**:
        - **produto**: Dados do novo produto a ser criado.
    - **Resposta**:
        - Dados do produto recém-criado.
    """
    if usuario_logado.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas administradores podem criar produtos.")

    return criar_produto(db, produto)


# 🔍 Listar todos os produtos ativos (Público ou Protegido)
@router.get("/", response_model=List[ProdutoResponse])
async def listar_produtos(
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Lista todos os produtos ativos.

    **Público**: Qualquer usuário pode listar produtos.

    - **Resposta**:
        - Lista de produtos ativos.
    """
    return listar_produtos_service(db)


# 🔍 Buscar um produto por ID (Público ou Protegido)
@router.get("/{produto_id}", response_model=ProdutoResponse)
async def buscar_produto(
        produto_id: int,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Busca um produto específico pelo ID.

    **Público**: Qualquer usuário pode buscar um produto pelo ID.

    - **Parâmetros**:
        - **produto_id**: ID do produto a ser buscado.
    - **Resposta**:
        - Dados do produto encontrado.
    """
    return buscar_produto_service(db, produto_id)


# 🔍 Buscar um produto completo (Público ou Protegido)
@router.get("/{produto_id}/completo", response_model=ProdutoResponse)
async def buscar_produto_completo(
        produto_id: int,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Busca um produto completo pelo ID.

    **Público**: Qualquer usuário pode buscar um produto completo pelo ID.

    - **Parâmetros**:
        - **produto_id**: ID do produto a ser buscado.
    - **Resposta**:
        - Dados do produto completo.
    """
    return buscar_produto_service(db, produto_id)


# ✏️ Editar um produto (Protegido por ADMIN)
@router.put("/{produto_id}/editar", response_model=ProdutoResponse)
async def editar_produto(
        produto_id: int,
        update_data: ProdutoUpdate,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Edita os dados de um produto existente.

    **Protegido**: Apenas administradores podem editar produtos.

    - **Parâmetros**:
        - **produto_id**: ID do produto a ser editado.
        - **update_data**: Dados para atualização do produto.
    - **Resposta**:
        - Dados do produto editado.
    """
    if usuario_logado.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas administradores podem editar produtos.")

    return atualizar_produto_service(db, produto_id, update_data.dict(exclude_unset=True))


# 🚫 Inativar um produto (Protegido por ADMIN)
@router.put("/{produto_id}/inativar", response_model=ProdutoResponse)
async def inativar_produto(
        produto_id: int,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por autenticação
):
    """
    Inativa um produto específico.

    **Protegido**: Apenas administradores podem inativar produtos.

    - **Parâmetros**:
        - **produto_id**: ID do produto a ser inativado.
    - **Resposta**:
        - Dados do produto inativado.
    """
    if usuario_logado.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas administradores podem inativar produtos.")

    return inativar_produto_service(db, produto_id)
