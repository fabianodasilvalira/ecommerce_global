from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.services import pagamento_service
from app.schemas import pagamento as pagamento_schema

router = APIRouter(
    prefix="/api/v1/pagamentos",
    tags=["pagamentos"],
)

@router.post("/", response_model=pagamento_schema.PagamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_pagamento(pagamento: pagamento_schema.PagamentoCreate, db: Session = Depends(get_db)):
    return pagamento_service.criar_pagamento(db, pagamento)

@router.get("/", response_model=List[pagamento_schema.PagamentoResponse])
def listar_pagamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return pagamento_service.listar_pagamentos(db, skip=skip, limit=limit)

@router.get("/{pagamento_id}", response_model=pagamento_schema.PagamentoResponse)
def buscar_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    return pagamento_service.buscar_pagamento(db, pagamento_id)

@router.put("/{pagamento_id}", response_model=pagamento_schema.PagamentoResponse)
def atualizar_pagamento(pagamento_id: int, pagamento_update: pagamento_schema.PagamentoUpdate, db: Session = Depends(get_db)):
    return pagamento_service.atualizar_pagamento(db, pagamento_id, pagamento_update)

@router.delete("/{pagamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    pagamento_service.deletar_pagamento(db, pagamento_id)
    return {"detail": "Pagamento excluído com sucesso"}
