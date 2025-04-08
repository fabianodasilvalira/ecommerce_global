from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.estoque import EstoqueCreate, EstoqueUpdate, EstoqueResponse
from app.services.estoque_service import (
    adicionar_estoque,
    obter_estoque,
    listar_estoque,
    atualizar_estoque,
    deletar_estoque
)

router = APIRouter()

@router.post("/", response_model=EstoqueResponse)
def adicionar_item_estoque(estoque_data: EstoqueCreate, db: Session = Depends(get_db)):
    return adicionar_estoque(db, estoque_data)

@router.get("/{produto_id}/produto/", response_model=EstoqueResponse)
def buscar_estoque(produto_id: int, db: Session = Depends(get_db)):
    return obter_estoque(db, produto_id)

@router.get("/", response_model=list[EstoqueResponse])
def listar_itens_estoque(db: Session = Depends(get_db)):
    return listar_estoque(db)

@router.put("/{produto_id}", response_model=EstoqueResponse)
def editar_estoque(produto_id: int, estoque_data: EstoqueUpdate, db: Session = Depends(get_db)):
    return atualizar_estoque(db, produto_id, estoque_data)

@router.delete("/{produto_id}")
def remover_item_estoque(produto_id: int, db: Session = Depends(get_db)):
    return deletar_estoque(db, produto_id)
