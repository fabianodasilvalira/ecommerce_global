from sqlalchemy.orm import Session, load_only, joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from decimal import Decimal
from sqlalchemy.orm import joinedload
from app.models import Usuario, ItemVenda
from app.models import Produto
from app.models import Cupom
from app.models.venda import StatusVendaEnum, Venda
from app.schemas.venda_schema import VendaCreate


def criar_venda(db: Session, venda: VendaCreate, usuario: Usuario) -> Venda:
    try:
        nova_venda = Venda(
            usuario_id=usuario.id,
            endereco_id=venda.endereco_id,
            cupom_id=venda.cupom_id,
            status=StatusVendaEnum.PENDENTE
        )

        total_venda = Decimal("0.00")
        desconto_percentual = Decimal("0.00")

        # Validação e cálculo do cupom
        if venda.cupom_id:
            cupom = db.query(Cupom).filter(Cupom.id == venda.cupom_id).first()
            if not cupom:
                raise HTTPException(status_code=404, detail="Cupom não encontrado.")
            if cupom.desconto:
                desconto_percentual = Decimal(str(cupom.desconto)) / Decimal("100.00")

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

            if not produto.estoque:
                raise HTTPException(status_code=400, detail=f"Produto '{produto.nome}' está sem estoque cadastrado.")

            if produto.estoque.quantidade < item.quantidade:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estoque insuficiente para '{produto.nome}'. Quantidade disponível: {produto.estoque.quantidade}."
                )

            # Validação: se cupom está presente, não pode ter promoção ativa
            if venda.cupom_id and produto.promocoes:
                for promocao in produto.promocoes:
                    if promocao.ativo and promocao.data_inicio <= datetime.now() <= promocao.data_fim:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Produto '{produto.nome}' está com promoção ativa. Não é permitido usar cupom junto com promoção."
                        )

            preco_com_desconto = produto.preco_final * (Decimal("1.00") - desconto_percentual)
            preco_unitario = preco_com_desconto.quantize(Decimal("0.01"))

            subtotal = preco_unitario * item.quantidade
            total_venda += subtotal

            item_venda = ItemVenda(
                produto_id=produto.id,
                quantidade=item.quantidade,
                preco_unitario=preco_unitario
            )

            nova_venda.itens.append(item_venda)

            # Atualiza estoque
            produto.estoque.quantidade -= item.quantidade

        nova_venda.total = total_venda.quantize(Decimal("0.01"))

        db.add(nova_venda)
        db.commit()
        db.refresh(nova_venda)

        return nova_venda

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao processar venda no banco de dados: {str(e)}")


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
        return venda  # vai retornar com todos os relacionamentos carregados
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao detalhar venda: {str(e)}")


