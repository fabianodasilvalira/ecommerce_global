from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.produto import Produto
from app.models.categoria import Categoria
from fastapi import HTTPException, status
import random
import string
import logging
from typing import Dict, Any, Optional

from app.schemas.produto_schema import ProdutoResponse

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


def criar_produto(db: Session, produto_data: Dict[str, Any]) -> ProdutoResponse:
    try:
        categoria_id = produto_data.get('categoria_id')

        # Verifica se a categoria existe
        if not db.query(Categoria).get(categoria_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria com ID {categoria_id} não encontrada"
            )

        # Verifica se o produto já existe (ativo ou inativo) na categoria
        produto_existente = db.query(Produto).filter(
            Produto.nome == produto_data['nome'],
            Produto.categoria_id == categoria_id
        ).first()

        if produto_existente:
            if produto_existente.ativo:
                # Caso o produto já esteja ativo, não permite duplicação
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Produto já cadastrado e ativo na mesma categoria"
                )
            else:
                # Caso o produto esteja inativo, atualiza ele e reativa
                produto_existente.ativo = True  # Reativa o produto
                produto_existente.preco = produto_data['preco']  # Atualiza o preço
                produto_existente.descricao = produto_data['descricao']  # Atualiza a descrição
                produto_existente.volume = produto_data.get('volume', produto_existente.volume)  # Atualiza o volume
                produto_existente.unidade_medida = produto_data.get('unidade_medida', produto_existente.unidade_medida)  # Atualiza unidade medida

                # Commit das alterações
                db.commit()
                db.refresh(produto_existente)

                # Calculando o preco_final
                preco_final = produto_existente.preco * 1.2  # Exemplo de cálculo com "imposto" de 20%

                # Retorna o produto atualizado com o preco_final calculado
                produto_response = ProdutoResponse(
                    id=produto_existente.id,
                    sku=produto_existente.sku,
                    nome=produto_existente.nome,
                    descricao=produto_existente.descricao,
                    preco=produto_existente.preco,
                    volume=produto_existente.volume,
                    unidade_medida=produto_existente.unidade_medida,
                    ativo=produto_existente.ativo,
                    categoria_id=produto_existente.categoria_id,
                    preco_final=preco_final  # Incluindo o preco_final no response
                )

                return produto_response

        # Caso não encontre um produto existente (ativo ou inativo), cria um novo produto
        sku = generate_sku(db, produto_data['nome'], categoria_id)

        # Calculando o preco_final
        preco_final = produto_data['preco'] * 1.2  # Exemplo de cálculo com "imposto" de 20%

        novo_produto = Produto(
            sku=sku,
            nome=produto_data['nome'],
            descricao=produto_data['descricao'],
            preco=produto_data['preco'],
            categoria_id=categoria_id,
            volume=produto_data.get('volume'),
            unidade_medida=produto_data.get('unidade_medida', 'ml'),
            ativo=produto_data.get('ativo', True)
        )

        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)

        # Retorne o produto com o preco_final calculado
        produto_response = ProdutoResponse(
            id=novo_produto.id,
            sku=novo_produto.sku,
            nome=novo_produto.nome,
            descricao=novo_produto.descricao,
            preco=novo_produto.preco,
            volume=novo_produto.volume,
            unidade_medida=novo_produto.unidade_medida,
            ativo=novo_produto.ativo,
            categoria_id=novo_produto.categoria_id,
            preco_final=preco_final  # Incluindo o preco_final no response
        )

        return produto_response
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Erro de integridade ao criar produto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar produto (dados inválidos ou duplicados)"
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
        preco_final = produto.preco * 1.2  # Exemplo de cálculo de preço final com 20% de imposto

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
            preco_final=preco_final  # Incluindo o preco_final no response
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
    preco_final = produto.preco * 1.2  # Ajuste conforme a lógica de preço final

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
