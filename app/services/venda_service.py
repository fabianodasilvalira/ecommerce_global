from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload, load_only
from app.models import Venda, ItemVenda, Produto, Cupom, Estoque, Pagamento
from app.models.pagamento import MetodoPagamentoEnum
from app.schemas.relatorio_pagamento import StatusPagamentoEnum
from app.schemas.venda_schema import VendaCreate
from app.models.venda import StatusVendaEnum, TipoDescontoEnum
from app.models.movimentacao_estoque import MovimentacaoEstoque, TipoMovimentoEnum
from app.models import Usuario, ItemVenda, Produto, Cupom
from app.models.venda import StatusVendaEnum, Venda, TipoDescontoEnum
from app.schemas.venda_schema import VendaCreate


def produto_possui_promocao_ativa(produto: Produto) -> bool:
    agora = datetime.now()
    return any(p.ativo and p.data_inicio <= agora <= p.data_fim for p in produto.promocoes)



from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from sqlalchemy.orm import Session, joinedload, load_only
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

# Assuma que as importações das models e enums já estão feitas corretamente

def criar_venda(db: Session, venda: VendaCreate, usuario) -> Venda:
    try:
        nova_venda = Venda(
            usuario_id=usuario.id,
            endereco_id=venda.endereco_id,
            cupom_id=venda.cupom_id,
            status=StatusVendaEnum.PENDENTE.value,
        )

        total_bruto = Decimal("0.00")
        total_com_desconto = Decimal("0.00")
        valor_desconto = Decimal("0.00")
        tipo_desconto = TipoDescontoEnum.NENHUM.value
        desconto_percentual = Decimal("0.00")

        if venda.cupom_id:
            cupom = db.query(Cupom).filter(Cupom.id == venda.cupom_id).first()
            if not cupom:
                raise HTTPException(status_code=404, detail="Cupom não encontrado.")
            if cupom.desconto:
                desconto_percentual = Decimal(str(cupom.desconto)) / Decimal("100.00")
                tipo_desconto = TipoDescontoEnum.CUPOM.value

        for item in venda.itens:
            produto = (
                db.query(Produto)
                .options(
                    load_only(Produto.id, Produto.nome, Produto.preco_final)
                )
                .options(
                    joinedload(Produto.estoque),
                    joinedload(Produto.promocoes)
                )
                .filter(Produto.id == item.produto_id)
                .first()
            )

            if not produto:
                raise HTTPException(status_code=404, detail=f"Produto ID {item.produto_id} não encontrado.")

            if not produto.estoque or produto.estoque.quantidade < item.quantidade:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estoque insuficiente para '{produto.nome}'. Quantidade disponível: {produto.estoque.quantidade if produto.estoque else 0}."
                )

            if venda.cupom_id and produto.promocoes and produto_possui_promocao_ativa(produto):
                raise HTTPException(
                    status_code=400,
                    detail=f"Produto '{produto.nome}' está com promoção ativa. Não é permitido usar cupom junto com promoção."
                )

            preco_bruto = Decimal(str(produto.preco_final))
            preco_unitario = preco_bruto

            if produto.promocoes and produto_possui_promocao_ativa(produto):
                promocao = produto.promocoes[0]
                tipo_desconto = TipoDescontoEnum.PROMOCAO.value

                if promocao.preco_promocional is not None:
                    preco_unitario = Decimal(str(promocao.preco_promocional))
                elif promocao.desconto_percentual is not None:
                    percentual = Decimal(str(promocao.desconto_percentual)) / Decimal("100.00")
                    preco_unitario = preco_bruto * (Decimal("1.00") - percentual)
                else:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Produto '{produto.nome}' está com promoção ativa, mas sem valor de desconto válido."
                    )
            elif desconto_percentual > 0:
                preco_unitario = preco_bruto * (Decimal("1.00") - desconto_percentual)

            preco_unitario = preco_unitario.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            subtotal_bruto = preco_bruto * item.quantidade
            subtotal_com_desconto = preco_unitario * item.quantidade

            total_bruto += subtotal_bruto
            total_com_desconto += subtotal_com_desconto

            item_venda = ItemVenda(
                produto_id=produto.id,
                quantidade=item.quantidade,
                preco_unitario=preco_unitario
            )
            nova_venda.itens.append(item_venda)

            produto.estoque.quantidade -= item.quantidade

            movimento = MovimentacaoEstoque(
                produto_id=produto.id,
                tipo_movimentacao=TipoMovimentoEnum.SAIDA,
                quantidade=item.quantidade,
                data=datetime.utcnow(),
                venda=nova_venda
            )
            db.add(movimento)

        valor_desconto = (total_bruto - total_com_desconto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        nova_venda.valor_total_bruto = total_bruto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        nova_venda.total = total_com_desconto.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        nova_venda.valor_desconto = valor_desconto
        nova_venda.tipo_desconto = tipo_desconto

        db.add(nova_venda)
        db.flush()  # garante o ID da venda para uso no pagamento

        # 4. Criar o pagamento após a venda estar salva (mas antes do commit final)
        pagamento = Pagamento(
            venda_id=nova_venda.id,
            valor=nova_venda.total,
            metodo_pagamento=MetodoPagamentoEnum.PIX,
            status=StatusPagamentoEnum.PENDENTE
        )
        db.add(pagamento)
        db.add(pagamento)

        db.commit()
        db.refresh(nova_venda)

        return nova_venda

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao processar venda: {str(e)}")


def cancelar_venda(db: Session, venda_id: int, usuario: Usuario):
    venda = db.query(Venda).filter(Venda.id == venda_id, Venda.usuario_id == usuario.id).first()

    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")

    if venda.status == StatusVendaEnum.CANCELADO:
        raise HTTPException(status_code=400, detail="Venda já está cancelada.")

    if venda.status == StatusVendaEnum.PAGO:
        raise HTTPException(status_code=400, detail="Não é possível cancelar uma venda já paga.")

    venda.status = StatusVendaEnum.CANCELADO
    db.commit()


def listar_vendas_usuario(db: Session, usuario: Usuario):
    try:
        vendas = (
            db.query(Venda)
            .options(
                joinedload(Venda.itens).joinedload(ItemVenda.produto),
                joinedload(Venda.cupom),
                joinedload(Venda.endereco)
            )
            .filter(Venda.usuario_id == usuario.id)
            .order_by(Venda.data_venda.desc())
            .all()
        )
        return vendas
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar vendas: {str(e)}")


def detalhar_venda(db: Session, venda_id: int, usuario: Usuario):
    try:
        venda = (
            db.query(Venda)
            .options(
                joinedload(Venda.usuario),
                joinedload(Venda.endereco),
                joinedload(Venda.cupom),
                joinedload(Venda.itens).joinedload(ItemVenda.produto)
            )
            .filter(Venda.id == venda_id, Venda.usuario_id == usuario.id)
            .first()
        )
        if not venda:
            raise HTTPException(status_code=404, detail="Venda não encontrada.")
        return venda
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao detalhar venda: {str(e)}")
