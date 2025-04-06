from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
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


def atualizar_usuario(db: Session, usuario_id: int, dados: UsuarioUpdate):
    usuario = obter_usuario(db, usuario_id)
    if not usuario:
        return None

    for attr, value in dados.dict(exclude_unset=True).items():
        if attr == "senha":
            setattr(usuario, attr, get_password_hash(value))
        else:
            setattr(usuario, attr, value)

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
