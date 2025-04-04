from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.produto_service import criar_produto
from app.models.produto import Produto
from app.models.categoria import Categoria
from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse, ProdutoUpdate

router = APIRouter()

# 1. Criar um novo produto
@router.post("/produtos/", response_model=ProdutoResponse)
def criar_novo_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    produto_criado = criar_produto(db, produto)
    return produto_criado

# 2. Listar todos os produtos
@router.get("/produtos/", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).filter(Produto.ativo == True).all()
    return produtos  # Produto já está no formato correto devido ao Pydantic

# 3. Buscar um produto por ID
@router.get("/produtos/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id, Produto.ativo == True).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado ou inativo")

    return produto  # ProdutoResponse já lida com a serialização

# 4. Editar um produto
@router.put("/produtos/{produto_id}/editar", response_model=ProdutoResponse)
def editar_produto(produto_id: int, update_data: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Verifica se a categoria existe, caso tenha sido alterada
    if update_data.categoria_id:
        categoria = db.query(Categoria).filter(Categoria.id == update_data.categoria_id).first()
        if not categoria:
            raise HTTPException(status_code=400, detail="Categoria não encontrada")

    # Atualiza os campos permitidos
    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(produto, field, value)

    # Atualiza preco_final se necessário
    if "preco" in update_dict or "margem_lucro" in update_dict:
        produto.atualizar_preco_final()

    db.commit()
    db.refresh(produto)

    return produto  # FastAPI converte automaticamente para ProdutoResponse

# 5. Inativar um produto
@router.put("/produtos/{produto_id}/inativar", response_model=ProdutoResponse)
def inativar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto.ativo = not produto.ativo
    db.commit()
    db.refresh(produto)

    return produto
