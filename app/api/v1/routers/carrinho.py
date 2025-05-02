from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models import Usuario
from app.models.pagamento import MetodoPagamentoEnum
from app.schemas.carrinho_schema import CarrinhoAtualizarInput, FinalizarCarrinhoRequest
from app.schemas.venda_schema import VendaResponse
from app.schemas import carrinho_schema as schemas
from app.services import carrinho_service

router = APIRouter()


@router.post("/adicionar", response_model=schemas.CarrinhoOut)
def adicionar_item(
    item: schemas.ItemCarrinhoBase,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return carrinho_service.adicionar_item_ao_carrinho(db, usuario.id, item)

@router.get("/", response_model=schemas.CarrinhoOut)
def ver_carrinho(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return carrinho_service.ver_carrinho(db, usuario.id)

@router.delete("/remover/{produto_id}", response_model=schemas.CarrinhoOut)
def remover_item(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return carrinho_service.remover_item_do_carrinho(db, usuario.id, produto_id)

@router.put("/atualizar/{produto_id}/produto", response_model=schemas.CarrinhoOut)
def atualizar_quantidade(
    produto_id: int,
    dados: schemas.CarrinhoAtualizarInput,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    quantidade = dados.itens[0].quantidade
    return carrinho_service.atualizar_quantidade_item(db, usuario.id, produto_id, quantidade)

@router.delete("/limpar", response_model=schemas.CarrinhoOut)
def limpar_carrinho(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return carrinho_service.limpar_carrinho(db, usuario.id)

@router.post("/finalizar_carrinho")
def finalizar_carrinho(
        payload: FinalizarCarrinhoRequest,
        db: Session = Depends(get_db),
        usuario: Usuario = Depends(get_current_user)
):
    try:

        # Validação adicional dos itens do carrinho
        if not payload.itens or len(payload.itens) == 0:
            raise HTTPException(status_code=400, detail="O carrinho não pode estar vazio")

        # Validação de pagamento com cartão
        if payload.metodo_pagamento in [MetodoPagamentoEnum.CARTAO_CREDITO, MetodoPagamentoEnum.CARTAO_DEBITO]:
            if not payload.bandeira_cartao or not payload.ultimos_digitos_cartao or not payload.nome_cartao:
                raise HTTPException(
                    status_code=400,
                    detail="Para pagamento com cartão, bandeira, dígitos finais e nome no cartão são obrigatórios"
                )
            if payload.metodo_pagamento == MetodoPagamentoEnum.CARTAO_CREDITO and not payload.numero_parcelas:
                raise HTTPException(
                    status_code=400,
                    detail="Número de parcelas é obrigatório para cartão de crédito"
                )

        # Chama o serviço de finalização do carrinho e criação de venda
        return carrinho_service.finalizar_carrinho_e_criar_venda(
            db=db,
            usuario_id=usuario.id,
            endereco_id=payload.endereco_id,
            cupom_id=payload.cupom_id,
            metodo_pagamento=payload.metodo_pagamento,
            numero_parcelas=payload.numero_parcelas,
            bandeira_cartao=payload.bandeira_cartao,
            ultimos_digitos_cartao=payload.ultimos_digitos_cartao,
            nome_cartao=payload.nome_cartao
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao finalizar o carrinho: {str(e)}")


@router.get("/historico", response_model=List[schemas.CarrinhoOut])
def listar_historico(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return carrinho_service.listar_carrinhos_finalizados(db, usuario.id)

@router.get("/item/{produto_id}", response_model=schemas.ItemCarrinhoOut)
def ver_item_carrinho(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return carrinho_service.ver_item_especifico(db, usuario.id, produto_id)

@router.get("/finalizados", response_model=List[schemas.CarrinhoOut])
def listar_carrinhos_finalizados(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return carrinho_service.listar_carrinhos_finalizados(db, usuario.id, skip, limit)