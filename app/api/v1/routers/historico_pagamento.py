from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.historico_pagamento import HistoricoPagamentoCreate, HistoricoPagamentoResponse
from app.services import historico_pagamento as crud

router = APIRouter()


@router.post("/", response_model=HistoricoPagamentoResponse)
def criar_historico(dados: HistoricoPagamentoCreate, db: Session = Depends(get_db)):
    return crud.criar_historico_pagamento(db, dados)

@router.get("/", response_model=list[HistoricoPagamentoResponse])
def listar(db: Session = Depends(get_db)):
    return crud.listar_historicos(db)

@router.get("/por-pagamento/{pagamento_id}", response_model=list[HistoricoPagamentoResponse])
def por_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    return crud.buscar_por_pagamento(db, pagamento_id)
