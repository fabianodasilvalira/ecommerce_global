from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload, load_only
from sqlalchemy import and_, func

from app.models import (
    Venda, ItemVenda, Produto, Cupom, Estoque,
    Pagamento, Endereco, Carrinho, Usuario,
    MovimentacaoEstoque
)
from app.models.pagamento import MetodoPagamentoEnum
from app.schemas.relatorio_pagamento import StatusPagamentoEnum
from app.schemas.venda_schema import VendaCreate, ItemVendaCreate, VendaOut
from app.models.venda import StatusVendaEnum, TipoDescontoEnum
from app.models.movimentacao_estoque import TipoMovimentoEnum

logger = logging.getLogger(__name__)


def produto_possui_promocao_ativa(produto: Produto) -> bool:
    """Verifica se o produto possui promoção ativa no momento atual."""
    agora = datetime.now()
    return any(
        p.ativo and p.data_inicio <= agora <= p.data_fim
        for p in produto.promocoes
    )


def criar_venda(db: Session, venda_data: VendaCreate, usuario: Usuario) -> VendaOut:
    """
    Cria uma nova venda com validações:
    - Estoque
    - Cupom/promoção (não acumulativos)
    - Movimentação de estoque
    - Pagamento pendente
    """
    try:
        nova_venda = Venda(
            usuario_id=usuario.id,
            endereco_id=venda_data.endereco_id,
            cupom_id=venda_data.cupom_id,
            status=StatusVendaEnum.PENDENTE.value,
            data_venda=datetime.utcnow()
        )

        total_bruto = Decimal("0.00")
        total_com_desconto = Decimal("0.00")
        tipo_desconto = TipoDescontoEnum.NENHUM.value
        desconto_percentual = Decimal("0.00")

        # Validação do cupom
        if venda_data.cupom_id:
            cupom = db.query(Cupom).get(venda_data.cupom_id)
            if not cupom:
                raise HTTPException(status_code=404, detail="Cupom não encontrado")
            if cupom.desconto:
                desconto_percentual = Decimal(str(cupom.desconto)) / Decimal("100.00")
                tipo_desconto = TipoDescontoEnum.CUPOM.value

        for item in venda_data.itens:
            produto = db.query(Produto).options(
                load_only(Produto.id, Produto.nome, Produto.preco_final),
                joinedload(Produto.estoque),
                joinedload(Produto.promocoes)
            ).filter(Produto.id == item.produto_id).first()

            if not produto:
                raise HTTPException(status_code=404, detail=f"Produto ID {item.produto_id} não encontrado")

            # Valida estoque
            estoque_disponivel = produto.estoque.quantidade if produto.estoque else 0
            if estoque_disponivel < item.quantidade:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estoque insuficiente para '{produto.nome}'. Disponível: {estoque_disponivel}"
                )

            # Conflito cupom + promoção
            if venda_data.cupom_id and produto_possui_promocao_ativa(produto):
                raise HTTPException(
                    status_code=400,
                    detail=f"Não é permitido usar cupom em produto com promoção ativa: {produto.nome}"
                )

            preco_unitario = calcular_preco_com_desconto(
                preco_bruto=Decimal(str(produto.preco_final)),
                produto=produto,
                desconto_percentual=desconto_percentual
            )

            subtotal_bruto = Decimal(str(produto.preco_final)) * item.quantidade
            subtotal_com_desconto = preco_unitario * item.quantidade
            total_bruto += subtotal_bruto
            total_com_desconto += subtotal_com_desconto

            item_venda = ItemVenda(
                produto_id=produto.id,
                quantidade=item.quantidade,
                preco_unitario=preco_unitario
            )
            nova_venda.itens.append(item_venda)

            # Atualiza estoque
            produto.estoque.quantidade -= item.quantidade

            # Movimentação de estoque
            db.add(MovimentacaoEstoque(
                produto_id=produto.id,
                tipo_movimentacao=TipoMovimentoEnum.SAIDA,
                quantidade=item.quantidade,
                data=datetime.utcnow(),
                venda=nova_venda
            ))

        valor_desconto = (total_bruto - total_com_desconto).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        nova_venda.valor_total_bruto = total_bruto.quantize(Decimal("0.01"))
        nova_venda.total = total_com_desconto.quantize(Decimal("0.01"))
        nova_venda.valor_desconto = valor_desconto
        nova_venda.tipo_desconto = tipo_desconto

        db.add(nova_venda)
        db.flush()  # gera o ID da venda para o pagamento

        # Cria o pagamento
        db.add(Pagamento(
            venda_id=nova_venda.id,
            valor=nova_venda.total,
            metodo_pagamento=MetodoPagamentoEnum.PIX,
            status=StatusPagamentoEnum.PENDENTE
        ))

        db.commit()
        db.refresh(nova_venda)

        return nova_venda  # retorna o modelo SQLAlchemy

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar venda: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar venda"
        )



def calcular_preco_com_desconto(
    preco_bruto: Decimal,
    produto: Produto,
    desconto_percentual: Decimal
) -> Decimal:
    """
    Retorna o preço com desconto de promoção ou cupom (não acumulativo).
    Promoção tem prioridade.
    """
    preco_final = preco_bruto

    if produto_possui_promocao_ativa(produto):
        promocao = next(p for p in produto.promocoes if p.ativo and p.data_inicio <= datetime.now() <= p.data_fim)
        if promocao.preco_promocional:
            preco_final = Decimal(str(promocao.preco_promocional))
        elif promocao.desconto_percentual:
            percentual = Decimal(str(promocao.desconto_percentual)) / Decimal("100.00")
            preco_final *= (1 - percentual)
    elif desconto_percentual > 0:
        preco_final *= (1 - desconto_percentual)

    return preco_final.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)



def cancelar_venda(db: Session, venda_id: int, usuario: Usuario) -> None:
    """Cancela uma venda se ainda não foi paga."""
    try:
        venda = db.query(Venda).filter(
            and_(
                Venda.id == venda_id,
                Venda.usuario_id == usuario.id,
                Venda.is_ativo == True
            )
        ).first()

        if not venda:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        if venda.status == StatusVendaEnum.CANCELADO:
            raise HTTPException(status_code=400, detail="Venda já está cancelada")
        if venda.status == StatusVendaEnum.PAGO:
            raise HTTPException(status_code=400, detail="Não é possível cancelar venda já paga")

        venda.status = StatusVendaEnum.CANCELADO
        venda.is_ativo = False
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erro ao cancelar venda {venda_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar cancelamento"
        )


def listar_vendas_usuario(
        db: Session,
        usuario: Usuario,
        limit: int = 100,
        offset: int = 0,
        apenas_ativas: bool = True
) -> List[Venda]:
    """Lista vendas do usuário com paginação."""
    try:
        query = db.query(Venda).options(
            joinedload(Venda.itens).options(
                load_only(ItemVenda.id, ItemVenda.quantidade, ItemVenda.preco_unitario),
                joinedload(ItemVenda.produto).load_only(Produto.id, Produto.nome)
            ),
            joinedload(Venda.cupom).load_only(Cupom.id, Cupom.codigo),
            joinedload(Venda.endereco).load_only(Endereco.id, Endereco.cep),
            joinedload(Venda.carrinho).load_only(Carrinho.id)
        ).filter(Venda.usuario_id == usuario.id)

        if apenas_ativas:
            query = query.filter(Venda.is_ativo == True)

        return query.order_by(
            Venda.data_venda.desc()
        ).offset(offset).limit(limit).all()

    except SQLAlchemyError as e:
        logger.error(f"Erro ao listar vendas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao recuperar histórico"
        )


def detalhar_venda(db: Session, venda_id: int, usuario: Usuario) -> Venda:
    """Obtém detalhes completos de uma venda específica."""
    try:
        venda = db.query(Venda).options(
            joinedload(Venda.usuario),
            joinedload(Venda.endereco),
            joinedload(Venda.cupom),
            joinedload(Venda.itens).joinedload(ItemVenda.produto),
            joinedload(Venda.carrinho),
            joinedload(Venda.pagamentos)
        ).filter(
            and_(
                Venda.id == venda_id,
                Venda.usuario_id == usuario.id
            )
        ).first()

        if not venda:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        return venda

    except SQLAlchemyError as e:
        logger.error(f"Erro ao detalhar venda {venda_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao recuperar dados da venda"
        )


def criar_venda_a_partir_do_carrinho(
        db: Session,
        carrinho: Carrinho,
        endereco_id: int,
        cupom_id: Optional[int] = None
) -> Venda:
    """Converte um carrinho em uma venda completa."""
    try:
        if carrinho.venda:
            raise HTTPException(
                status_code=400,
                detail="Este carrinho já foi convertido em venda"
            )

        if not carrinho.itens:
            raise HTTPException(
                status_code=400,
                detail="Carrinho vazio"
            )

        # Marca carrinho como finalizado
        carrinho.is_finalizado = True
        carrinho.atualizado_em = func.now()

        # Cria a venda
        venda = criar_venda(
            db=db,
            venda_data=VendaCreate(
                endereco_id=endereco_id,
                cupom_id=cupom_id,
                itens=[
                    ItemVendaCreate(
                        produto_id=item.produto_id,
                        quantidade=item.quantidade
                    ) for item in carrinho.itens
                ]
            ),
            usuario=carrinho.usuario
        )

        # Estabelece relação
        venda.carrinho_id = carrinho.id
        carrinho.venda = venda

        db.commit()
        return venda

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar venda do carrinho: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao finalizar compra"
        )