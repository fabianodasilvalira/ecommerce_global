from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import func, and_
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app import models
from app.models import carrinho as carrinho_model, Venda, Produto
from app.models import item_carrinho as item_model
from app.models import produto as produto_model
from app.models.carrinho import Carrinho
from app.models.item_carrinho import ItemCarrinho
from app.schemas.carrinho_schema import ItemCarrinhoBase
from app.schemas.venda_schema import VendaCreate, ItemVendaCreate
from app.services import venda_service
from app.services.produto_service import logger

def buscar_ou_criar_carrinho(db: Session, usuario_id: int):
    return (
        db.query(Carrinho)
        .options(
            joinedload(Carrinho.itens)
            .joinedload(ItemCarrinho.produto)
            .joinedload(Produto.imagens),
            joinedload(Carrinho.itens)
            .joinedload(ItemCarrinho.produto)
            .joinedload(Produto.categoria)
        )
        .filter_by(usuario_id=usuario_id, is_finalizado=False)
        .first()
    )


def calcular_totais(carrinho):
    # Formata os itens do carrinho
    itens_formatados = []
    for item in carrinho.itens:
        itens_formatados.append({
            "id": item.id,
            "quantidade": item.quantidade,
            "valor_unitario": float(item.valor_unitario),
            "valor_total": float(item.valor_total),
            "produto": formatar_produto(item.produto)
        })

    # Calcula totais
    subtotal = sum(float(item.valor_total) for item in carrinho.itens)
    total = subtotal  # Ou subtotal + taxas - descontos
    data_finalizacao = carrinho.data_finalizacao if carrinho.data_finalizacao else None  # Garante que será None se não finalizado

    return {
        "id": carrinho.id,
        "usuario_id": carrinho.usuario_id,
        "itens": itens_formatados,
        "subtotal": float(subtotal),
        "total": float(total),
        "is_finalizado": carrinho.is_finalizado,
        "data_finalizacao": data_finalizacao  # Retorna o campo de data_finalizacao
    }



def adicionar_item_ao_carrinho(db: Session, usuario_id: int, item_data: ItemCarrinhoBase):
    # Verificar se a quantidade é válida
    if item_data.quantidade <= 0:
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")

    # Buscar o produto
    produto = db.query(produto_model.Produto).filter_by(id=item_data.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Verificar estoque, se o produto possui o atributo de estoque
    if hasattr(produto, 'estoque_disponivel') and produto.estoque_disponivel < item_data.quantidade:
        raise HTTPException(status_code=400, detail="Quantidade indisponível em estoque")

    # Buscar ou criar o carrinho do usuário
    carrinho = buscar_ou_criar_carrinho(db, usuario_id)

    # Verificar se o item já está no carrinho
    item = db.query(item_model.ItemCarrinho).filter_by(
        carrinho_id=carrinho.id,
        produto_id=item_data.produto_id
    ).first()

    # Se o item já existe no carrinho, apenas atualiza a quantidade e o valor total
    if item:
        item.quantidade += item_data.quantidade
        item.valor_total = item.quantidade * item.valor_unitario
    else:
        # Caso o item não exista no carrinho, cria um novo item
        item = item_model.ItemCarrinho(
            carrinho_id=carrinho.id,
            produto_id=item_data.produto_id,
            quantidade=item_data.quantidade,
            valor_unitario=produto.preco,
            valor_total=produto.preco * item_data.quantidade
        )
        db.add(item)

    # Salvar as alterações no banco de dados
    db.commit()
    db.refresh(carrinho)

    # Calcular os totais atualizados do carrinho
    return calcular_totais(buscar_ou_criar_carrinho(db, usuario_id))


def remover_item_do_carrinho(db: Session, usuario_id: int, produto_id: int):
    carrinho = buscar_ou_criar_carrinho(db, usuario_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")

    item = db.query(item_model.ItemCarrinho).filter_by(
        carrinho_id=carrinho.id,
        produto_id=produto_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    db.delete(item)
    db.commit()
    return calcular_totais(buscar_ou_criar_carrinho(db, usuario_id))


def atualizar_quantidade_item(db: Session, usuario_id: int, produto_id: int, quantidade: int):
    if quantidade < 1:
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")

    carrinho = buscar_ou_criar_carrinho(db, usuario_id)

    item = db.query(item_model.ItemCarrinho).filter_by(
        carrinho_id=carrinho.id,
        produto_id=produto_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    item.quantidade = quantidade
    item.valor_total = item.valor_unitario * quantidade

    db.commit()
    return calcular_totais(buscar_ou_criar_carrinho(db, usuario_id))


def limpar_carrinho(db: Session, usuario_id: int):
    carrinho = buscar_ou_criar_carrinho(db, usuario_id)
    for item in carrinho.itens:
        db.delete(item)
    db.commit()
    return calcular_totais(buscar_ou_criar_carrinho(db, usuario_id))


def ver_carrinho(db: Session, usuario_id: int) -> Dict[str, Any]:
    carrinho = buscar_ou_criar_carrinho(db, usuario_id)
    if not carrinho:
        carrinho = Carrinho(usuario_id=usuario_id)
        db.add(carrinho)
        db.commit()
        db.refresh(carrinho)

    itens_formatados = []
    for item in carrinho.itens:
        produto_formatado = formatar_produto(item.produto)
        itens_formatados.append({
            "id": item.id,
            "quantidade": item.quantidade,
            "valor_unitario": float(item.valor_unitario),
            "valor_total": float(item.valor_total),
            "produto": produto_formatado
        })
    import json
    print("Dados do carrinho:", json.dumps({
        "itens": itens_formatados,
        "subtotal": sum(item.valor_total for item in carrinho.itens)
    }, indent=2, default=str))
    return {
        "id": carrinho.id,
        "usuario_id": carrinho.usuario_id,
        "is_finalizado": carrinho.is_finalizado,
        "itens": itens_formatados,
        "subtotal": float(sum(item.valor_total for item in carrinho.itens)),
        "data_finalizacao": carrinho.data_finalizacao if carrinho.data_finalizacao else None

    }


def formatar_produto(produto: Produto) -> Dict[str, Any]:
    """Formata os dados do produto para o schema"""

    # Verifica se há imagens e pega a primeira URL
    imagem_url = ""
    if produto.imagens and len(produto.imagens) > 0:
        imagem_url = produto.imagens[0].imagem_url  # Pega a URL da primeira imagem

    # Obtém o nome da categoria ou string vazia
    categoria_nome = ""
    if produto.categoria:
        categoria_nome = produto.categoria.nome  # Acessa o atributo 'nome' do objeto Categoria

    return {
        "id": produto.id,
        "nome": produto.nome,
        "descricao": produto.descricao,
        "preco": float(produto.preco),  # Ou preco_final, conforme o modelo
        "imagem_url": imagem_url,  # Agora sempre será uma string
        "categoria": {
            "id": produto.categoria.id,
            "nome": produto.categoria.nome,
            "descricao": produto.categoria.descricao,
            "ativo": produto.categoria.ativo
        } if produto.categoria else None    }


def finalizar_carrinho(db: Session, usuario_id: int):
    carrinho = (
        db.query(carrinho_model.Carrinho)
        .filter_by(usuario_id=usuario_id, is_finalizado=False)
        .first()
    )

    if not carrinho or not carrinho.itens:
        raise HTTPException(status_code=400, detail="Carrinho vazio ou não encontrado")

    carrinho.is_finalizado = True
    carrinho.data_finalizacao = func.now()  # Preenche com a data e hora atual
    db.commit()
    db.refresh(carrinho)
    return calcular_totais(carrinho)


def listar_carrinhos_finalizados(
    db: Session,
    usuario_id: int,
    skip: int = 0,
    limit: int = 100
):
    try:
        carrinhos = (
            db.query(models.Carrinho)
            .options(
                joinedload(models.Carrinho.itens)
                .joinedload(models.ItemCarrinho.produto)
                .joinedload(models.Produto.imagens),
                joinedload(models.Carrinho.itens)
                .joinedload(models.ItemCarrinho.produto)
                .joinedload(models.Produto.categoria)
            )
            .filter(
                models.Carrinho.usuario_id == usuario_id,
                models.Carrinho.is_finalizado == True
            )
            .order_by(models.Carrinho.data_finalizacao.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        if not carrinhos:
            raise HTTPException(
                status_code=404,
                detail="Nenhum carrinho finalizado encontrado para este usuário"
            )

        return [calcular_totais(carrinho) for carrinho in carrinhos]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar carrinhos finalizados: {str(e)}"
        )


def ver_item_especifico(db: Session, usuario_id: int, produto_id: int):
    carrinho = buscar_ou_criar_carrinho(db, usuario_id)

    item = (
        db.query(item_model.ItemCarrinho)
        .options(
            joinedload(item_model.ItemCarrinho.produto)
            .joinedload(produto_model.Produto.imagens),
            joinedload(item_model.ItemCarrinho.produto)
            .joinedload(produto_model.Produto.categoria)
        )
        .filter_by(carrinho_id=carrinho.id, produto_id=produto_id)
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    # Formatar a resposta conforme o schema esperado
    return {
        "id": item.id,
        "quantidade": item.quantidade,
        "valor_unitario": float(item.valor_unitario),
        "valor_total": float(item.valor_total),
        "produto": {
            "id": item.produto.id,
            "nome": item.produto.nome,
            "descricao": item.produto.descricao,
            "preco": float(item.produto.preco),
            "imagem_url": item.produto.imagens[0].imagem_url if item.produto.imagens else "",
            "categoria": {
                "id": item.produto.categoria.id,
                "nome": item.produto.categoria.nome,
                "descricao": item.produto.categoria.descricao,
                "ativo": item.produto.categoria.ativo
            } if item.produto.categoria else None        }
    }


def finalizar_carrinho_e_criar_venda(
        db: Session,
        usuario_id: int,
        endereco_id: int,
        cupom_id: Optional[int] = None
) -> Venda:

    carrinho = db.query(Carrinho).filter(
        Carrinho.usuario_id == usuario_id,
        Carrinho.is_finalizado == False
    ).first()
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado ou já finalizado")

    try:
        # 1. Busca e bloqueia APENAS o carrinho (sem joins)
        carrinho = db.query(Carrinho).filter(
            and_(
                Carrinho.usuario_id == usuario_id,
                Carrinho.is_finalizado == False
            )
        ).with_for_update().first()

        if not carrinho:
            raise HTTPException(status_code=404, detail="Carrinho ativo não encontrado")

        # 2. Agora carrega os relacionamentos necessários
        carrinho = db.query(Carrinho).options(
            joinedload(Carrinho.itens).joinedload(ItemCarrinho.produto),
            joinedload(Carrinho.usuario)
        ).filter(Carrinho.id == carrinho.id).first()

        if not carrinho.itens:
            raise HTTPException(status_code=400, detail="Carrinho vazio")

        # Finaliza carrinho
        carrinho.is_finalizado = True
        carrinho.data_finalizacao = func.now()
        carrinho.atualizado_em = func.now()

        # Cria venda
        venda = venda_service.criar_venda_a_partir_do_carrinho(
            db=db,
            carrinho=carrinho,
            endereco_id=endereco_id,
            cupom_id=cupom_id
        )

        db.commit()
        return venda

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao finalizar carrinho: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao processar finalização do carrinho"
        )
