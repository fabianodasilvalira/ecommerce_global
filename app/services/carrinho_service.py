from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any

from sqlalchemy import func, and_
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app import models
from app.models import carrinho as carrinho_model, Venda, Produto, Usuario
from app.models import item_carrinho as item_model
from app.models import produto as produto_model
from app.models.carrinho import Carrinho
from app.models.item_carrinho import ItemCarrinho
from app.models.pagamento import MetodoPagamentoEnum, Pagamento, StatusPagamento
from app.schemas.carrinho_schema import ItemCarrinhoBase, CarrinhoOut
from app.schemas.venda_schema import VendaCreate, ItemVendaCreate
from app.services import venda_service
from app.services.produto_service import logger
from app.services.venda_service import criar_venda_a_partir_do_carrinho, criar_venda


def buscar_ou_criar_carrinho(db: Session, usuario_id: int):
    # Verifica apenas se o carrinho não finalizado já existe
    carrinho = (
        db.query(carrinho_model.Carrinho)
        .filter_by(usuario_id=usuario_id, is_finalizado=False)
        .first()
    )

    if not carrinho:
        carrinho = carrinho_model.Carrinho(
            usuario_id=usuario_id,
            is_finalizado=False,
            criado_em=datetime.now()  # ou datetime.utcnow() dependendo do padrão do seu projeto
        )
        db.add(carrinho)
        db.commit()
        db.refresh(carrinho)

    return carrinho



def calcular_totais(carrinho):
    # Formata os itens do carrinho
    itens_formatados = []
    for item in carrinho.itens:
        itens_formatados.append({
            "id": item.id,
            "quantidade": item.quantidade,
            "valor_unitario": float(item.valor_unitario),
            "valor_total": float(item.valor_total),
            "produto": formatar_produto(item.produto),
            "data_finalizacao": carrinho.data_finalizacao

        })

    # Calcula totais
    subtotal = sum(float(item.valor_total) for item in carrinho.itens)
    total = subtotal  # Ou subtotal + taxas - descontos, se aplicável
    data_finalizacao = carrinho.data_finalizacao if carrinho.data_finalizacao else None

    return {
        "id": carrinho.id,
        "usuario_id": carrinho.usuario_id,
        "itens": itens_formatados,
        "subtotal": float(subtotal),
        "total": float(total),
        "is_finalizado": carrinho.is_finalizado,
        "data_finalizacao": data_finalizacao
    }


def adicionar_item_ao_carrinho(db: Session, usuario_id: int, item_data: ItemCarrinhoBase):
    # Verificar se a quantidade é válida
    if item_data.quantidade <= 0:
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")

    # Buscar o produto
    produto = db.query(Produto).filter(Produto.id == item_data.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Verificar estoque
    if hasattr(produto, 'estoque') and produto.estoque.quantidade < item_data.quantidade:
        raise HTTPException(status_code=400, detail="Quantidade indisponível em estoque")

    # Buscar ou criar carrinho
    carrinho = buscar_ou_criar_carrinho(db, usuario_id)

    # Verificar se item já existe no carrinho
    item_existente = db.query(ItemCarrinho).filter(ItemCarrinho.carrinho_id == carrinho.id, ItemCarrinho.produto_id == item_data.produto_id ).first()

    if item_existente:
        # Atualizar item existente
        item_existente.quantidade += item_data.quantidade
        item_existente.valor_total = produto.preco_final * item_existente.quantidade
    else:
        # Criar novo item
        novo_item = ItemCarrinho(
            carrinho_id=carrinho.id,
            produto_id=item_data.produto_id,
            quantidade=item_data.quantidade,
            valor_unitario=produto.preco_final,
            valor_total=produto.preco_final * item_data.quantidade
        )
        db.add(novo_item)

    db.commit()
    return calcular_totais(carrinho)


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
        "preco_final": float(produto.preco_final),  # ✅ necessário
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

    if not carrinho:
        raise HTTPException(status_code=404, detail="carrinho não encontrado")

    produto = db.query(produto_model.Produto).filter_by(id=produto_id).first()

    # Se o produto não for encontrado, levanta uma exceção
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    # Tenta buscar o item diretamente

    item = db.query(item_model.ItemCarrinho).filter(
        item_model.ItemCarrinho.carrinho_id == carrinho.id,
        item_model.ItemCarrinho.produto_id == produto_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    return item  # Agora pode retornar o item diretamente



def finalizar_carrinho_e_criar_venda(
    db: Session,
    usuario_id: int,
    endereco_id: int,
    cupom_id: Optional[int] = None,
    metodo_pagamento: [str] = None,
    numero_parcelas: Optional[int] = None,
    bandeira_cartao: Optional[str] = None,
    ultimos_digitos_cartao: Optional[str] = None,
    nome_cartao: Optional[str] = None
) -> Venda:
    """Finaliza o carrinho e cria uma venda com os dados adicionais de pagamento."""

    # Busca o carrinho ativo
    carrinho = db.query(Carrinho).filter(
        Carrinho.usuario_id == usuario_id,
        Carrinho.is_finalizado == False
    ).first()

    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado ou já finalizado")

    try:
        # Bloqueia o carrinho para evitar concorrência
        carrinho = db.query(Carrinho).filter(
            and_(
                Carrinho.usuario_id == usuario_id,
                Carrinho.is_finalizado == False
            )
        ).with_for_update().first()

        if not carrinho:
            raise HTTPException(status_code=404, detail="Carrinho ativo não encontrado")

        # Carrega os itens do carrinho e o usuário
        carrinho = db.query(Carrinho).options(
            joinedload(Carrinho.itens).joinedload(ItemCarrinho.produto),
            joinedload(Carrinho.usuario)
        ).filter(Carrinho.id == carrinho.id).first()

        if not carrinho.itens:
            raise HTTPException(status_code=400, detail="Carrinho vazio")

        # Monta os itens para a venda
        itens_venda = [
            ItemVendaCreate(
                produto_id=item.produto_id,
                quantidade=item.quantidade,
            )
            for item in carrinho.itens
        ]

        # Monta o objeto de entrada para criação da venda
        venda_data = VendaCreate(
            endereco_id=endereco_id,
            cupom_id=cupom_id,
            itens=itens_venda,
            carrinho_id=carrinho.id,  # Passando o ID do carrinho, não o objeto
            metodo_pagamento=metodo_pagamento,
            numero_parcelas=numero_parcelas,
            bandeira_cartao=bandeira_cartao,
            ultimos_digitos_cartao=ultimos_digitos_cartao,
            nome_cartao=nome_cartao
        )

        # Cria a venda
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

        venda = criar_venda(
            db=db,
            venda_data=venda_data,
            usuario=usuario,
        )

        # Finaliza o carrinho
        carrinho.is_finalizado = True
        carrinho.data_finalizacao = datetime.now()

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



