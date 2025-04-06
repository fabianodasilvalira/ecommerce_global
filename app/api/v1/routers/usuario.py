from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioOut
from app.services import usuario_service
from typing import List

router = APIRouter()

@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(ativos: bool = Query(True), db: Session = Depends(get_db)):
    return usuario_service.listar_usuarios(db, ativos)


@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_service.listar_usuarios(db)


@router.get("/{usuario_id}", response_model=UsuarioOut)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuario_service.obter_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioOut)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = usuario_service.atualizar_usuario(db, usuario_id, dados)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.delete("/{usuario_id}", response_model=UsuarioOut)
def inativar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuario_service.inativar_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario
