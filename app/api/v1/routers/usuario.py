# FastAPI
from fastapi import APIRouter, Depends, HTTPException, Query, status

# Banco de dados e models
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.usuario import TipoUsuarioEnum, Usuario


# Schemas e services
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioOut, UsuarioUpdateAdmin
from app.services import usuario_service
from app.services.auth import obter_usuario_logado

router = APIRouter()


# 📌 Criar novo usuário (público)
@router.post("/", response_model=UsuarioOut, status_code=201)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if usuario_service.obter_por_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    return usuario_service.criar_usuario(db, usuario)


# 🔍 Listar usuários ativos/inativos (⚠️ Pode ser público ou protegido, dependendo da regra do seu sistema)
@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(
        ativos: bool = Query(True),
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por token
):
    return usuario_service.listar_usuarios(db, ativos)


# ✏️ Atualizar usuário (verifica se é o próprio usuário ou ADMIN)
@router.put("/{usuario_id}", response_model=UsuarioOut)
def atualizar_usuario(
        usuario_id: int,
        dados: UsuarioUpdate,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)
):
    if usuario_logado.id != usuario_id and usuario_logado.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")

    usuario = usuario_service.atualizar_usuario(db, usuario_id, dados, usuario_logado)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


# 🚫 Inativar usuário (apenas se logado; você pode adicionar uma regra para ADMIN apenas, se quiser)
@router.delete("/{usuario_id}", response_model=UsuarioOut)
def inativar_usuario(
        usuario_id: int,
        db: Session = Depends(get_db),
        usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido
):
    # Exemplo: só o ADMIN pode inativar
    if usuario_logado.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas administradores podem inativar usuários.")

    usuario = usuario_service.inativar_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario
