from fastapi import APIRouter, Depends, HTTPException, Query, status, Security
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.usuario import TipoUsuarioEnum, Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioOut, UsuarioUpdateAdmin
from app.services import usuario_service
from app.services.auth import obter_usuario_logado

router = APIRouter()

# 📌 Criar novo usuário (público)
@router.post("/", response_model=UsuarioOut, status_code=201)
async def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo usuário no sistema.

    **Público**: Qualquer pessoa pode criar um usuário.

    - **Parâmetros**:
        - **usuario**: Objeto contendo os dados para criar o usuário.
    - **Resposta**:
        - Retorna os dados do usuário recém-criado.
    """
    if usuario_service.obter_por_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    return usuario_service.criar_usuario(db, usuario)

# 🔍 Listar usuários ativos/inativos (⚠️ Pode ser público ou protegido, dependendo da regra do seu sistema)
@router.get("/", response_model=List[UsuarioOut])
async def listar_usuarios(
    ativos: bool = Query(True, description="Filtra por usuários ativos ou inativos."),
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(obter_usuario_logado)  # Protegido por token
):
    """
    Lista usuários ativos ou inativos.

    **Protegido**: Apenas usuários autenticados podem acessar a lista de usuários.

    - **Parâmetros**:
        - **ativos**: (bool) Filtro para usuários ativos ou inativos.
    - **Resposta**:
        - Lista de usuários (ativos ou inativos).
    """
    return usuario_service.listar_usuarios(db, ativos)

# ✏️ Atualizar usuário (verifica se é o próprio usuário ou ADMIN)
@router.put("/{usuario_id}", response_model=UsuarioOut)
async def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(obter_usuario_logado)
):
    """
    Atualiza os dados de um usuário.

    **Protegido**: Somente o próprio usuário ou administradores podem atualizar os dados.

    - **Parâmetros**:
        - **usuario_id**: ID do usuário a ser atualizado.
        - **dados**: Dados que serão atualizados.
    - **Resposta**:
        - Dados do usuário atualizado.
    """
    if usuario_logado.id != usuario_id and usuario_logado.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")

    usuario = usuario_service.atualizar_usuario(db, usuario_id, dados, usuario_logado)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

# 🚫 Inativar usuário (apenas se logado; você pode adicionar uma regra para ADMIN apenas, se quiser)
@router.delete("/{usuario_id}", response_model=UsuarioOut)
async def inativar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Security(obter_usuario_logado)  # Protegido
):
    """
    Inativa um usuário do sistema.

    **Protegido**: Apenas administradores podem inativar usuários.

    - **Parâmetros**:
        - **usuario_id**: ID do usuário a ser inativado.
    - **Resposta**:
        - Dados do usuário inativado.
    """
    if usuario_logado.tipo_usuario != TipoUsuarioEnum.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Apenas administradores podem inativar usuários.")

    usuario = usuario_service.inativar_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario
