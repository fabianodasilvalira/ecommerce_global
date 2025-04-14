
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.db.database import get_db
from app.schemas.venda_schema import VendaCreate, VendaResponse, VendaDetalhadaResponse, VendaOut
from app.services.venda_service import criar_venda, listar_vendas_usuario, detalhar_venda, cancelar_venda
from app.models.usuario import Usuario

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_venda_endpoint(
    venda: VendaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return criar_venda(db=db, venda=venda, usuario=usuario)

@router.get("/usuario", response_model=List[VendaResponse])
def listar_vendas_usuario_endpoint(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return listar_vendas_usuario(db=db, usuario=usuario)

@router.get("/{venda_id}", response_model=VendaOut)
def detalhar_venda_endpoint(
    venda_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    return detalhar_venda(db, venda_id, usuario)

@router.delete("/{venda_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancelar_venda_endpoint(
    venda_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    cancelar_venda(db=db, venda_id=venda_id, usuario=usuario)
    return None
