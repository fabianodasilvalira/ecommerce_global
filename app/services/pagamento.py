from sqlalchemy.orm import Session
from app.models.pagamento import Pagamento
from app.schemas.relatorio_pagamento import FiltroRelatorioPagamento

def gerar_relatorio_pagamento(db: Session, filtro: FiltroRelatorioPagamento):
    query = db.query(Pagamento)

    if filtro.metodo_pagamento:
        query = query.filter(Pagamento.metodo_pagamento == filtro.metodo_pagamento)
    if filtro.status:
        query = query.filter(Pagamento.status == filtro.status)
    if filtro.data_inicio:
        query = query.filter(Pagamento.criado_em >= filtro.data_inicio)
    if filtro.data_fim:
        query = query.filter(Pagamento.criado_em <= filtro.data_fim)

    return query.order_by(Pagamento.criado_em.desc()).all()
