from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.pagamento import Pagamento
from app.models.historico_pagamento import HistoricoPagamento

# 1. Relatório por método de pagamento
def relatorio_por_metodo_pagamento(db: Session):
    return db.query(
        Pagamento.metodo_pagamento,
        func.count(Pagamento.id).label("total")
    ).group_by(Pagamento.metodo_pagamento).all()

# 2. Relatório por status
def relatorio_por_status(db: Session):
    return db.query(
        Pagamento.status,
        func.count(Pagamento.id).label("total")
    ).group_by(Pagamento.status).all()

# 3. Relatório por dia
def relatorio_por_dia(db: Session):
    return db.query(
        func.date(Pagamento.criado_em).label("data"),
        func.count(Pagamento.id).label("total")
    ).group_by(func.date(Pagamento.criado_em)).order_by(func.date(Pagamento.criado_em)).all()

# 4. Relatório filtrado
def relatorio_filtrado(db: Session, metodo: str, status: str, inicio, fim):
    return db.query(Pagamento).filter(
        Pagamento.metodo_pagamento == metodo,
        Pagamento.status == status,
        Pagamento.criado_em >= inicio,
        Pagamento.criado_em <= fim
    ).order_by(Pagamento.criado_em).all()
