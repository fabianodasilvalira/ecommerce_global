from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from passlib.context import CryptContext
from app.services.auth import obter_usuario_logado

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def criar_usuario(db: Session, usuario_data: UsuarioCreate):
    db_usuario = Usuario(
        nome=usuario_data.nome,
        email=usuario_data.email,
        senha=get_password_hash(usuario_data.senha),
        cpf_cnpj=usuario_data.cpf_cnpj,
        telefone=usuario_data.telefone,
        tipo_usuario=usuario_data.tipo_usuario
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def listar_usuarios(db: Session, ativos: bool = True):
    return db.query(Usuario).filter(Usuario.ativo == ativos).all()

def obter_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def atualizar_usuario(
    db: Session,
    usuario_id: int,
    dados: UsuarioUpdate,
    usuario_logado: Usuario
):
    usuario = obter_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # ✅ Verifica permissões
    if usuario_logado.id != usuario.id and usuario_logado.tipo_usuario != "admin":
        raise HTTPException(status_code=403, detail="Você não tem permissão para atualizar este usuário")

    # ✅ Atualiza campos se fornecidos
    if dados.nome is not None:
        usuario.nome = dados.nome
    if dados.email is not None:
        usuario.email = dados.email
    if dados.cpf_cnpj is not None:
        usuario.cpf_cnpj = dados.cpf_cnpj
    if dados.telefone is not None:
        usuario.telefone = dados.telefone
    if dados.tipo_usuario is not None and usuario_logado.tipo_usuario == "admin":
        usuario.tipo_usuario = dados.tipo_usuario  # Apenas admin pode alterar tipo
    if dados.senha is not None:
        usuario.senha = get_password_hash(dados.senha)

    db.commit()
    db.refresh(usuario)
    return usuario

def inativar_usuario(db: Session, usuario_id: int):
    usuario = obter_usuario(db, usuario_id)
    if not usuario:
        return None
    usuario.ativo = False
    db.commit()
    return usuario

def obter_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()
