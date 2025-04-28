import os
from dotenv import load_dotenv

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.database import get_db
from app.models.usuario import Usuario, TipoUsuarioEnum
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from passlib.context import CryptContext
from app.services.auth import obter_usuario_logado

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()

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
    if dados.ativo is not None and usuario_logado.tipo_usuario == "admin":
        usuario.ativo = dados.ativo

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


def criar_usuario_admin(db: Session):
    # Verificar se já existe um usuário ADMIN
    admin_existente = db.query(Usuario).filter(Usuario.tipo_usuario == TipoUsuarioEnum.ADMIN).first()

    if admin_existente:
        return  # Se já existir, não cria outro usuário ADMIN

    # Se não existir, cria o usuário administrador
    usuario_admin = Usuario(
        nome="Administrador",
        email=os.getenv("ADMIN_EMAIL"),  # Carrega o email do admin a partir da variável de ambiente
        senha=get_password_hash(os.getenv("ADMIN_PASSWORD")),  # Hash da senha do admin
        cpf_cnpj="12345678901",  # Adapte conforme necessário
        tipo_usuario=TipoUsuarioEnum.ADMIN,
    )

    try:
        db.add(usuario_admin)  # Adiciona o novo usuário à sessão
        db.commit()  # Realiza o commit para salvar a transação
        db.refresh(usuario_admin)  # Atualiza o objeto do usuário com os dados do banco
        print(f"Usuário administrador {usuario_admin.email} criado com sucesso.")
    except Exception as e:
        db.rollback()  # Reverte a transação em caso de erro
        print(f"Erro ao criar usuário administrador: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar usuário administrador")