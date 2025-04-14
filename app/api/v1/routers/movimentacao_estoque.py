from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.movimentacao_estoque import MovimentacaoEstoqueOut, MovimentacaoEstoqueCreate
from app.services import movimentacao_estoque as service

router = APIRouter()

@router.post("/", response_model=MovimentacaoEstoqueOut, status_code=status.HTTP_201_CREATED)
def criar_movimentacao(movimentacao: MovimentacaoEstoqueCreate, db: Session = Depends(get_db)):
    return service.criar_movimentacao_estoque(db, movimentacao)

@router.get("/", response_model=List[MovimentacaoEstoqueOut])
def listar_movimentacoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.listar_movimentacoes(db, skip=skip, limit=limit)
