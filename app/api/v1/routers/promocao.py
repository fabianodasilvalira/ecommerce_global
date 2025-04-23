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

@router.post("/", response_model=PromocaoResponse)
def criar_promocao(promocao: PromocaoCreate, db: Session = Depends(get_db)):
    # Chama o serviço de criação da promoção
    try:
        return criar_promocao_service(db, promocao)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[PromocaoResponse])
def listar_promocoes_ativas(db: Session = Depends(get_db)):
    # Chama o serviço para listar promoções ativas
    return listar_promocoes_ativas_service(db)

@router.get("/{promocao_id}", response_model=PromocaoResponse)
def buscar_promocao(promocao_id: int, db: Session = Depends(get_db)):
    # Chama o serviço para buscar uma promoção pelo ID
    return buscar_promocao_service(db, promocao_id)

@router.put("/{promocao_id}/editar", response_model=PromocaoResponse)
def editar_promocao(promocao_id: int, update_data: PromocaoUpdate, db: Session = Depends(get_db)):
    # Chama o serviço para editar a promoção
    try:
        return editar_promocao_service(db, promocao_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{promocao_id}/inativar", response_model=PromocaoResponse)
def inativar_promocao(promocao_id: int, db: Session = Depends(get_db)):
    # Chama o serviço para inativar uma promoção
    try:
        return inativar_promocao_service(db, promocao_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
