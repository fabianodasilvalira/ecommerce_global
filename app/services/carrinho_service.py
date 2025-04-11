from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models import carrinho as carrinho_model
from app.models import item_carrinho as item_model
from app.models import produto as produto_model
from app.models.carrinho import Carrinho
from app.schemas.carrinho_schema import ItemCarrinhoBase


def buscar_ou_criar_carrinho(db: Session, usuario_id: int):
    carrinho = (
        db.query(carrinho_model.Carrinho)
        .options(joinedload(carrinho_model.Carrinho.itens).joinedload(item_model.ItemCarrinho.produto))
        .filter_by(usuario_id=usuario_id, is_finalizado=False)
        .first()
    )
    if not carrinho:
        carrinho = carrinho_model.Carrinho(usuario_id=usuario_id)
        db.add(carrinho)
        db.commit()
        db.refresh(carrinho)
        carrinho.itens = []
    return carrinho


def calcular_totais(carrinho):
    total_valor = sum(float(item.valor_total) for item in carrinho.itens)
    carrinho.subtotal = round(total_valor, 2)
    return carrinho


def adicionar_item_ao_carrinho(db: Session, usuario_id: int, item_data: ItemCarrinhoBase):
    produto = db.query(produto_model.Produto).filter_by(id=item_data.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    carrinho = buscar_ou_criar_carrinho(db, usuario_id)

    item = db.query(item_model.ItemCarrinho).filter_by(
        carrinho_id=carrinho.id,
        produto_id=item_data.produto_id
    ).first()

    if item:
        item.quantidade += item_data.quantidade
        item.valor_total = item.quantidade * item.valor_unitario
    else:
        item = item_model.ItemCarrinho(
            carrinho_id=carrinho.id,
            produto_id=item_data.produto_id,
            quantidade=item_data.quantidade,
            valor_unitario=produto.preco,
            valor_total=produto.preco * item_data.quantidade
        )
        db.add(item)

    db.commit()
    db.refresh(carrinho)
    return calcular_totais(buscar_ou_criar_carrinho(db, usuario_id))


def remover_item_do_carrinho(db: Session, usuario_id: int, produto_id: int):
    carrinho = buscar_ou_criar_carrinho(db, usuario_id)

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


def ver_carrinho(db: Session, usuario_id: int):
    carrinho = buscar_ou_criar_carrinho(db, usuario_id)
    itens = carrinho.itens

    subtotal = sum(item.valor_total for item in itens)

    itens_response = []
    for item in itens:
        produto = item.produto
        imagem_url = produto.imagens[0].url if produto.imagens else ""

        itens_response.append({
            "id": item.id,
            "quantidade": item.quantidade,
            "valor_unitario": float(item.valor_unitario),
            "valor_total": float(item.valor_total),
            "produto": {
                "id": produto.id,
                "nome": produto.nome,
                "descricao": produto.descricao,
                "preco": float(produto.preco_final),
                "imagem_url": imagem_url,
                "categoria": produto.categoria.nome if produto.categoria else ""
            }
        })

    return {
        "id": carrinho.id,
        "usuario_id": carrinho.usuario_id,
        "is_finalizado": carrinho.is_finalizado,
        "itens": itens_response,
        "subtotal": float(subtotal)
    }



def finalizar_carrinho(db: Session, usuario_id: int):
    carrinho = (
        db.query(carrinho_model.Carrinho)
        .filter_by(usuario_id=usuario_id, is_finalizado=False)
        .first()
    )

    if not carrinho or not carrinho.itens:
        raise HTTPException(status_code=400, detail="Carrinho vazio ou não encontrado")

    carrinho.is_finalizado = True
    db.commit()
    db.refresh(carrinho)
    return calcular_totais(carrinho)


def listar_carrinhos_finalizados(db: Session, usuario_id: int):
    carrinhos = (
        db.query(carrinho_model.Carrinho)
        .options(joinedload(carrinho_model.Carrinho.itens).joinedload(item_model.ItemCarrinho.produto))
        .filter_by(usuario_id=usuario_id, is_finalizado=True)
        .all()
    )

    for carrinho in carrinhos:
        calcular_totais(carrinho)

    return carrinhos


def ver_item_especifico(db: Session, usuario_id: int, produto_id: int):
    carrinho = buscar_ou_criar_carrinho(db, usuario_id)

    item = (
        db.query(item_model.ItemCarrinho)
        .options(joinedload(item_model.ItemCarrinho.produto))
        .filter_by(carrinho_id=carrinho.id, produto_id=produto_id)
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    return item
