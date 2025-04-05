from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.endereco import EnderecoCreate, EnderecoUpdate, EnderecoOut
from app.services import endereco_service

router = APIRouter(prefix="/enderecos", tags=["Endereços"])


@router.post("/", response_model=EnderecoOut)
def criar(endereco: EnderecoCreate, db: Session = Depends(get_db)):
    return endereco_service.criar_endereco(db, endereco)


@router.get("/", response_model=list[EnderecoOut])
def listar(usuario_id: int = None, db: Session = Depends(get_db)):
    return endereco_service.listar_enderecos(db, usuario_id)


@router.get("/{endereco_id}", response_model=EnderecoOut)
def buscar(endereco_id: int, db: Session = Depends(get_db)):
    endereco = endereco_service.buscar_endereco(db, endereco_id)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco


@router.put("/{endereco_id}/editar", response_model=EnderecoOut)
def atualizar(endereco_id: int, dados: EnderecoUpdate, db: Session = Depends(get_db)):
    endereco = endereco_service.atualizar_endereco(db, endereco_id, dados)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco


@router.delete("/{endereco_id}/inativar")
def inativar(endereco_id: int, db: Session = Depends(get_db)):
    endereco = endereco_service.inativar_endereco(db, endereco_id)
    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado ou já inativado")
    return {"ok": True, "msg": "Endereço inativado com sucesso"}

