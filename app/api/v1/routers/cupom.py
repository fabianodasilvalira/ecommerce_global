from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Cupom
from app.schemas.cupom_schema import CupomCreate, CupomResponse, CupomUpdate
from app.services.cupom_service import criar_cupom, listar_cupons, buscar_cupom_por_codigo, desativar_cupom, \
    atualizar_cupom_por_id, atualizar_cupom_por_codigo

router = APIRouter()


@router.post("/cupons/", response_model=CupomResponse)
def adicionar_cupom(cupom_data: CupomCreate, db: Session = Depends(get_db)):
    """ Adiciona um novo cupom """
    if buscar_cupom_por_codigo(db, cupom_data.codigo):
        raise HTTPException(status_code=400, detail="Código de cupom já existe")

    return criar_cupom(db, cupom_data)


# ✅ Atualizar cupom por ID
@router.put("/cupons/{cupom_id}", response_model=CupomResponse)
def editar_cupom_por_id(cupom_id: int, cupom_data: CupomUpdate, db: Session = Depends(get_db)):
    cupom = atualizar_cupom_por_id(db, cupom_id, cupom_data)
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return cupom

# ✅ Atualizar cupom por Código
@router.put("/cupons/codigo/{codigo}", response_model=CupomResponse)
def editar_cupom_por_codigo(codigo: str, cupom_data: CupomUpdate, db: Session = Depends(get_db)):
    cupom = atualizar_cupom_por_codigo(db, codigo, cupom_data)
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return cupom


@router.get("/cupons/", response_model=list[CupomResponse])
def listar_todos_cupons(db: Session = Depends(get_db)):
    """ Retorna todos os cupons cadastrados """
    return listar_cupons(db)


@router.get("/cupons/{codigo}", response_model=CupomResponse)
def buscar_cupom(codigo: str, db: Session = Depends(get_db)):
    """ Busca um cupom pelo código """
    cupom = buscar_cupom_por_codigo(db, codigo)
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")

    return cupom


@router.put("/cupons/{cupom_id}/desativar", response_model=CupomResponse)
def desativar_cupom_por_id(cupom_id: int, db: Session = Depends(get_db)):
    """ Desativa um cupom existente """
    cupom = desativar_cupom(db, cupom_id)
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")

    return cupom
