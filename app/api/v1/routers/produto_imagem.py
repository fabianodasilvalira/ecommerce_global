from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.produto_imagem_schema import (
    ProdutoImagemCreate,
    ProdutoImagemResponse,
    ProdutoImagemUpdate
)
from app.services.produto_imagem_service import (
    criar_imagem_produto,
    listar_imagens_produto,
    buscar_imagem_produto,
    deletar_imagem_produto,
    editar_imagem_produto
)

router = APIRouter()

# 📌 Endpoint para criar uma nova imagem de produto
@router.post("/", response_model=ProdutoImagemResponse, status_code=status.HTTP_201_CREATED)
def criar_imagem(imagem: ProdutoImagemCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova imagem associada a um produto.

    - **imagem**: Dados necessários para criar a imagem do produto.
    """
    return criar_imagem_produto(db, imagem)


# 📌 Endpoint para atualizar uma imagem de produto existente
@router.put("/{imagem_id}")
def atualizar_imagem(imagem_id: int, imagem_data: ProdutoImagemUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de uma imagem de produto existente.

    - **imagem_id**: ID da imagem a ser atualizada.
    - **imagem_data**: Dados atualizados para a imagem.
    """
    imagem = editar_imagem_produto(db, imagem_id, imagem_data)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return imagem


# 📌 Endpoint para listar as imagens de um produto específico
@router.get("/produto/{produto_id}", response_model=List[ProdutoImagemResponse])
def listar_imagens(produto_id: int, db: Session = Depends(get_db)):
    """
    Lista todas as imagens associadas a um produto específico.

    - **produto_id**: ID do produto para buscar suas imagens.
    """
    return listar_imagens_produto(db, produto_id)


# 📌 Endpoint para buscar uma imagem específica por ID
@router.get("/{imagem_id}", response_model=ProdutoImagemResponse)
def buscar_imagem(imagem_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de uma imagem de produto específica.

    - **imagem_id**: ID da imagem a ser buscada.
    """
    imagem = buscar_imagem_produto(db, imagem_id)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return imagem


# 📌 Endpoint para deletar uma imagem de produto
@router.delete("/{imagem_id}", response_model=ProdutoImagemResponse)
def deletar_imagem(imagem_id: int, db: Session = Depends(get_db)):
    """
    Remove uma imagem de produto pelo seu ID.

    - **imagem_id**: ID da imagem a ser removida.
    """
    imagem = deletar_imagem_produto(db, imagem_id)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return imagem
