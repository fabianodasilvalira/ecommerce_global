from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.produto import Produto
from app.models.categoria import Categoria
from app.schemas.produto_schema import ProdutoResponse, ProdutoCreate
from app.schemas.promocao_schema import PromocaoOut
from app.models.promocao import Promocao
from datetime import datetime  # ✅ Importado para verificar data atual


import random
import string
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def generate_sku(db: Session, nome: str, categoria_id: int) -> str:
    max_attempts = 5
    attempt = 0

    categoria = db.query(Categoria).get(categoria_id)
    categoria_nome = categoria.nome if categoria else "GEN"

    while attempt < max_attempts:
        prefixo = nome[:3].upper() if nome else "PRD"
        cat_prefix = categoria_nome[:3].upper()
        random_code = ''.join(random.choices(string.digits, k=4))
        sku = f"{prefixo}-{cat_prefix}-{random_code}"

        if not db.query(Produto).filter(Produto.sku == sku).first():
            return sku

        attempt += 1
        logger.warning(f"Tentativa {attempt}: SKU {sku} já existe. Gerando novo...")

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Não foi possível gerar um SKU único após várias tentativas"
    )

def criar_produto(db: Session, produto_data: ProdutoCreate) -> ProdutoResponse:
    try:
        categoria_id = produto_data.categoria_id

        # Verifica se a categoria existe
        categoria = db.query(Categoria).filter_by(id=categoria_id).first()
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria com ID {categoria_id} não encontrada"
            )

        # Verifica se o produto já existe na categoria
        produto_existente = db.query(Produto).filter(
            Produto.nome == produto_data.nome,
            Produto.categoria_id == categoria_id
        ).first()

        if produto_existente:
            if produto_existente.ativo:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Produto já cadastrado e ativo na mesma categoria"
                )
            else:
                # Atualiza e reativa o produto inativo
                produto_existente.ativo = True
                produto_existente.preco = produto_data.preco
                produto_existente.descricao = produto_data.descricao
                produto_existente.volume = produto_data.volume or produto_existente.volume
                produto_existente.unidade_medida = produto_data.unidade_medida or produto_existente.unidade_medida
                produto_existente.margem_lucro = produto_existente.margem_lucro if produto_existente.margem_lucro is not None else 20.0
                produto_existente.preco_final = produto_existente.preco * (1 + produto_existente.margem_lucro / 100)

                db.commit()
                db.refresh(produto_existente)

                return ProdutoResponse.model_validate(produto_existente)

        # Criando um novo produto
        sku = generate_sku(db, produto_data.nome, categoria_id)

        margem_lucro = produto_data.margem_lucro if produto_data.margem_lucro is not None else 20.0
        preco_final = produto_data.preco * (1 + margem_lucro / 100)

        novo_produto = Produto(
            sku=sku,
            nome=produto_data.nome,
            descricao=produto_data.descricao,
            preco=produto_data.preco,
            categoria_id=categoria_id,
            volume=produto_data.volume,
            unidade_medida=produto_data.unidade_medida if produto_data.unidade_medida else None,
            ativo=produto_data.ativo if produto_data.ativo is not None else True,
            margem_lucro=margem_lucro,
            preco_final=preco_final
        )

        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)

        return ProdutoResponse.model_validate(novo_produto)

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar produto: possíveis dados duplicados ou inválidos"
        )

def listar_produtos_service(db: Session) -> List[ProdutoResponse]:
    produtos = db.query(Produto).filter(Produto.ativo == True).all()
    return [ProdutoResponse.model_validate(prod) for prod in produtos]


def listar_produtos_com_destaques_service(db: Session) -> Dict[str, List[ProdutoResponse]]:
    produtos_ativos = db.query(Produto).filter(Produto.ativo == True).all()

    # Separar os produtos em destaque (tem um ProdutoDestaque associado)
    destaques = [p for p in produtos_ativos if p.destaque is not None]
    comuns = [p for p in produtos_ativos if p.destaque is None]

    return {
        "destaques": [ProdutoResponse.model_validate(p) for p in destaques],
        "produtos": [ProdutoResponse.model_validate(p) for p in comuns]
    }


def buscar_produto_service(db: Session, produto_id: int) -> ProdutoResponse:
    produto = (
        db.query(Produto)
        .options(
            joinedload(Produto.categoria),
            joinedload(Produto.imagens),
            joinedload(Produto.promocoes),
            joinedload(Produto.estoque)
        )
        .filter(Produto.id == produto_id, Produto.ativo == True)
        .first()
    )

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado ou inativo")

    # Prepara os dados para a resposta
    produto_data = ProdutoResponse.model_validate(produto)

    # Adiciona informações de estoque se existir
    if produto.estoque:
        produto_data.estoque_disponivel = produto.estoque.quantidade

    # Filtra apenas promoções ativas
    agora = datetime.utcnow()
    produto_data.promocoes_ativas = [
        promocao for promocao in produto.promocoes
        if promocao.ativo and promocao.data_inicio <= agora <= promocao.data_fim
    ]

    return produto_data

def atualizar_produto_service(db: Session, produto_id: int, update_data: Dict[str, Any]) -> ProdutoResponse:
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if "categoria_id" in update_data:
        if not db.query(Categoria).filter_by(id=update_data["categoria_id"]).first():
            raise HTTPException(status_code=400, detail="Categoria não encontrada")

    for field, value in update_data.items():
        setattr(produto, field, value)

    produto.preco_final = produto.preco * (1 + (produto.margem_lucro or 20) / 100)

    db.commit()
    db.refresh(produto)

    return produto

def inativar_produto_service(db: Session, produto_id: int) -> ProdutoResponse:
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto.ativo = not produto.ativo
    db.commit()
    db.refresh(produto)

    return produto
