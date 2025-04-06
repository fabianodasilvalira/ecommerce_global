from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import get_db
from app.services import historico_pagamento as hp

router = APIRouter()

@router.get("/metodo-pagamento")
def get_por_metodo(db: Session = Depends(get_db)):
    return hp.relatorio_por_metodo_pagamento(db)

@router.get("/status")
def get_por_status(db: Session = Depends(get_db)):
    return hp.relatorio_por_status(db)

@router.get("/por-dia")
def get_por_dia(db: Session = Depends(get_db)):
    return hp.relatorio_por_dia(db)

@router.get("/filtrado")
def get_filtrado(
    metodo: str,
    status: str,
    inicio: datetime = Query(..., alias="data_inicio"),
    fim: datetime = Query(..., alias="data_fim"),
    db: Session = Depends(get_db)
):
    return hp.relatorio_filtrado(db, metodo, status, inicio, fim)
