from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.produto import Produto
from app.models.categoria import Categoria
from fastapi import HTTPException, status
import random
import string
import logging
from typing import Dict, Any, Optional

from app.schemas.produto_schema import ProdutoResponse, ProdutoCreate

logger = logging.getLogger(__name__)

def generate_sku(db: Session, nome: str, categoria_id: int) -> str:
    """
    Gera um SKU único verificando colisões no banco de dados.

    Args:
        db: Sessão do banco de dados
        nome: Nome do produto
        categoria_id: ID da categoria

    Returns:
        str: SKU único no formato PREFIX-CAT-1234
    """
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
        logger.error(f"Erro de integridade ao criar produto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar produto: possíveis dados duplicados ou inválidos"
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar produto: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Produto já cadastrado e ativo na mesma categoria"
        )

def atualizar_produto_service(db: Session, produto_id: int, update_data: Dict[str, Any]) -> ProdutoResponse:
    """
    Atualiza um produto existente.

    Args:
        db: Sessão do banco de dados
        produto_id: ID do produto a ser atualizado
        update_data: Dicionário com campos para atualizar

    Returns:
        ProdutoResponse: O produto atualizado com preco_final calculado
    """
    try:
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )

        # Verifica se a nova categoria existe (se for fornecida)
        if 'categoria_id' in update_data:
            if not db.query(Categoria).get(update_data['categoria_id']):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Categoria não encontrada"
                )

        # Atualiza os campos
        for field, value in update_data.items():
            setattr(produto, field, value)

        db.commit()
        db.refresh(produto)

        # Calculando o preco_final
        margem_lucro = update_data.get('margem_lucro', produto.margem_lucro or 20.0)  # Default 20%
        produto.preco_final = produto.preco * (1 + margem_lucro / 100)

        produto_response = ProdutoResponse(
            id=produto.id,
            sku=produto.sku,
            nome=produto.nome,
            descricao=produto.descricao,
            preco=produto.preco,
            volume=produto.volume,
            unidade_medida=produto.unidade_medida,
            ativo=produto.ativo,
            categoria_id=produto.categoria_id,
            preco_final=produto.preco_final
        )

        return produto_response

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro de integridade ao atualizar produto: {str(e)}"
        )

def inativar_produto_service(db: Session, produto_id: int) -> ProdutoResponse:
    """
    Inativa um produto no sistema.

    Args:
        db: Sessão do banco de dados
        produto_id: ID do produto a ser inativado

    Returns:
        ProdutoResponse: Produto inativado
    """
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    # Alterando o status para inativo
    produto.ativo = False

    db.commit()
    db.refresh(produto)

    # Retorna o produto com o preco_final calculado
    margem_lucro = produto.margem_lucro or 20.00  # Usa a margem definida no produto ou 20% como padrão
    preco_final = produto.preco * (1 + (margem_lucro / 100))

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
        preco_final=preco_final
    )
