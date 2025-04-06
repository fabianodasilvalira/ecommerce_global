from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.historico_pagamento import (
    HistoricoPagamentoCreate,
    HistoricoPagamentoResponse
)
from app.services import historico_pagamento as crud

router = APIRouter()


# 🧾 Criar novo histórico de pagamento
@router.post("/", response_model=HistoricoPagamentoResponse, summary="Criar histórico de pagamento")
def criar_historico_pagamento(
    dados: HistoricoPagamentoCreate,
    db: Session = Depends(get_db)
):
    return crud.criar_historico_pagamento(db, dados)


# 📜 Listar todos os históricos
@router.get("/", response_model=List[HistoricoPagamentoResponse], summary="Listar históricos de pagamento")
def listar_historicos_pagamento(db: Session = Depends(get_db)):
    return crud.listar_historicos(db)


# 🔍 Buscar históricos por ID de pagamento
@router.get("/por-pagamento/{pagamento_id}", response_model=List[HistoricoPagamentoResponse], summary="Buscar históricos por pagamento")
def buscar_historico_por_pagamento(
    pagamento_id: int,
    db: Session = Depends(get_db)
):
    return crud.buscar_por_pagamento(db, pagamento_id)
