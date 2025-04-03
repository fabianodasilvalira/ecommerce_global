from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal

from app.db.database import get_db
from app.services.produto_service import criar_produto
from app.models.produto import Produto
from app.models.categoria import Categoria
from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse, ProdutoUpdate

router = APIRouter()

# 1. Criar um novo produto
@router.post("/produtos/", response_model=ProdutoResponse)
def criar_novo_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    produto_criado = criar_produto(db, produto)  # Aceita diretamente ProdutoCreate
    return produto_criado

# 2. Listar todos os produtos
@router.get("/produtos/", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).filter(Produto.ativo == True).all()
    return [
        ProdutoResponse(
            id=produto.id,
            sku=produto.sku,
            nome=produto.nome,
            descricao=produto.descricao,
            preco=produto.preco,
            volume=produto.volume,
            unidade_medida=produto.unidade_medida,
            ativo=produto.ativo,
            categoria_id=produto.categoria_id,
            margem_lucro=produto.margem_lucro,
            preco_final=produto.calcular_preco_final()  # Usa o método da classe
        ) for produto in produtos
    ]

# 3. Buscar um produto por ID
@router.get("/produtos/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id, Produto.ativo == True).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado ou inativo")

    return ProdutoResponse(
        id=produto.id,
        sku=produto.sku,
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        volume=produto.volume,
        unidade_medida=produto.unidade_medida,
        ativo=produto.ativo,
        categoria_id=produto.categoria_id,
        margem_lucro=produto.margem_lucro,
        preco_final=produto.calcular_preco_final()  # Usa o método da classe
    )

# 4. Atualizar um produto
@router.put("/produtos/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, produto_dados: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Verifica se a categoria existe antes de atualizar o produto
    if produto_dados.categoria_id:
        categoria_existente = db.query(Categoria).filter(Categoria.id == produto_dados.categoria_id).first()
        if not categoria_existente:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

    for key, value in produto_dados.dict(exclude_unset=True).items():
        setattr(produto, key, value)

    db.commit()
    db.refresh(produto)

    return ProdutoResponse(
        id=produto.id,
        sku=produto.sku,
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        volume=produto.volume,
        unidade_medida=produto.unidade_medida,
        ativo=produto.ativo,
        categoria_id=produto.categoria_id,
        margem_lucro=produto.margem_lucro,
        preco_final=produto.calcular_preco_final()  # Usa o método da classe
    )

# 5. Inativar um produto
@router.put("/produtos/inativar/{produto_id}", response_model=ProdutoResponse)
def inativar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto.ativo = False  # Define o status do produto como inativo
    db.commit()
    db.refresh(produto)

    return ProdutoResponse(
        id=produto.id,
        sku=produto.sku,
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        volume=produto.volume,
        unidade_medida=produto.unidade_medida,
        ativo=produto.ativo,
        categoria_id=produto.categoria_id,
        margem_lucro=produto.margem_lucro,
        preco_final=produto.calcular_preco_final()  # Usa o método da classe
    )
