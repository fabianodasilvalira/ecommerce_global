from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.promocao_service import (
    criar_promocao_service,
    listar_promocoes_ativas_service,
    buscar_promocao_service,
    editar_promocao_service,
    inativar_promocao_service
)
from app.schemas.promocao_schema import PromocaoCreate, PromocaoResponse, PromocaoUpdate

router = APIRouter()

# Criar uma nova promoção
@router.post("/promocoes/", response_model=PromocaoResponse)
def criar_promocao(promocao: PromocaoCreate, db: Session = Depends(get_db)):
    return criar_promocao_service(db, promocao)

# Listar todas as promoções ativas
@router.get("/promocoes/", response_model=List[PromocaoResponse])
def listar_promocoes_ativas(db: Session = Depends(get_db)):
    return listar_promocoes_ativas_service(db)

# Buscar promoção por ID
@router.get("/promocoes/{promocao_id}", response_model=PromocaoResponse)
def buscar_promocao(promocao_id: int, db: Session = Depends(get_db)):
    return buscar_promocao_service(db, promocao_id)

# Editar uma promoção
@router.put("/promocoes/{promocao_id}/editar", response_model=PromocaoResponse)
def editar_promocao(promocao_id: int, update_data: PromocaoUpdate, db: Session = Depends(get_db)):
    return editar_promocao_service(db, promocao_id, update_data)

# Inativar uma promoção
@router.put("/promocoes/{promocao_id}/inativar", response_model=PromocaoResponse)
def inativar_promocao(promocao_id: int, db: Session = Depends(get_db)):
    return inativar_promocao_service(db, promocao_id)
