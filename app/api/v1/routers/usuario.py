# FastAPI
from fastapi import APIRouter, Depends, HTTPException, Query

# Banco de dados e models
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.usuario import TipoUsuarioEnum, Usuario

# Autenticação e Permissões
from app.dependencies.auth import obter_usuario_logado
from app.dependencies.permissoes import permitir_admin
from app.core.permissoes import permissao_necessaria

# Schemas e services
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioOut, UsuarioUpdateAdmin
from app.services import usuario_service
from app.services.usuario_service import atualizar_meu_usuario

router = APIRouter()

# ================================================
# ✅ Rotas públicas
# ================================================

# 📌 Criar novo usuário (público)
@router.post("/", response_model=UsuarioOut, status_code=201)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if usuario_service.obter_por_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    return usuario_service.criar_usuario(db, usuario)

# ================================================
# 👤 Ações do próprio usuário (autenticado)
# ================================================

# 👤 Atualizar os próprios dados
@router.put("/me", response_model=UsuarioOut)
def atualizar_me(
    dados: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(obter_usuario_logado)
):
    usuario = usuario_service.atualizar_meu_usuario(db, usuario_logado.id, dados)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario

# ================================================
# 🔐 Ações administrativas (admin)
# ================================================

# 🔐 Atualizar qualquer usuário (admin)
@router.put("/admin/{usuario_id}", response_model=UsuarioOut)
def atualizar_usuario_admin(
    usuario_id: int,
    dados: UsuarioUpdateAdmin,
    db: Session = Depends(get_db)
):
    usuario = usuario_service.atualizar_usuario_admin(db, usuario_id, dados)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario

# 👥 Listar todos os usuários (somente admin)
@router.get("/admin", summary="Listar todos os usuários (somente admin)")
def listar_todos_os_usuarios(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(permissao_necessaria(TipoUsuarioEnum.ADMIN))
):
    return db.query(Usuario).all()

# 🔧 Rota de teste admin
@router.get("/admin/teste")
def rota_teste():
    return {"rota": "funcionando"}

# ================================================
# 📋 Listagem e ações genéricas
# ================================================

# 🔍 Listar usuários ativos/inativos
@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(ativos: bool = Query(True), db: Session = Depends(get_db)):
    return usuario_service.listar_usuarios(db, ativos)

# 🔎 Obter usuário por ID
@router.get("/{usuario_id}", response_model=UsuarioOut)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuario_service.obter_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# ✏️ Atualizar usuário (sem regra de permissão definida)
@router.put("/{usuario_id}", response_model=UsuarioOut)
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = usuario_service.atualizar_usuario(db, usuario_id, dados)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# 🚫 Inativar usuário (soft delete)
@router.delete("/{usuario_id}", response_model=UsuarioOut)
def inativar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuario_service.inativar_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario
