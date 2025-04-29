from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.pagamento import Pagamento, StatusPagamento
from app.models.venda import Venda
from app.schemas.pagamento_schema import PagamentoCreate, PagamentoUpdate, PagamentoResponse

def criar_pagamento(db: Session, pagamento: PagamentoCreate) -> PagamentoResponse:
    # 🛡️ Verificar se a venda existe antes de criar o pagamento
    venda = db.query(Venda).filter(Venda.id == pagamento.venda_id).first()
    if not venda:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Venda não encontrada para o ID informado."
        )

    db_pagamento = Pagamento(
        venda_id=pagamento.venda_id,
        valor=pagamento.valor,
        metodo_pagamento=pagamento.metodo_pagamento,
        transacao_id=pagamento.transacao_id,
        status=StatusPagamento.PENDENTE,  # Sempre inicia como PENDENTE
    )
    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)

    # Retorna o pagamento com o formato correto de resposta
    return PagamentoResponse.from_orm(db_pagamento)

def listar_pagamentos(db: Session, skip: int = 0, limit: int = 100) -> list[PagamentoResponse]:
    pagamentos = db.query(Pagamento).offset(skip).limit(limit).all()
    return [PagamentoResponse.from_orm(pagamento) for pagamento in pagamentos]

def buscar_pagamento(db: Session, pagamento_id: int) -> PagamentoResponse:
    pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    if not pagamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado."
        )
    return PagamentoResponse.from_orm(pagamento)

def atualizar_pagamento(db: Session, pagamento_id: int, pagamento_update: PagamentoUpdate) -> PagamentoResponse:
    pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    if not pagamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado para atualização."
        )

    if pagamento_update.status is not None:
        pagamento.status = pagamento_update.status
    if pagamento_update.transacao_id is not None:
        pagamento.transacao_id = pagamento_update.transacao_id

    db.commit()
    db.refresh(pagamento)
    return PagamentoResponse.from_orm(pagamento)

def deletar_pagamento(db: Session, pagamento_id: int) -> PagamentoResponse:
    pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    if not pagamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pagamento não encontrado para exclusão."
        )

    db.delete(pagamento)
    db.commit()
    return PagamentoResponse.from_orm(pagamento)
