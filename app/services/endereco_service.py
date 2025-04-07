from sqlalchemy.orm import Session
from app.models import Endereco
from app.schemas.endereco import EnderecoCreate, EnderecoUpdate


def criar_endereco(db: Session, endereco: EnderecoCreate):
    novo_endereco = Endereco(**endereco.dict())
    db.add(novo_endereco)
    db.commit()
    db.refresh(novo_endereco)
    return novo_endereco


def listar_enderecos(db: Session, usuario_id: int = None):
    if usuario_id:
        return db.query(Endereco).filter(Endereco.usuario_id == usuario_id).all()
    return db.query(Endereco).all()


def buscar_endereco(db: Session, endereco_id: int):
    return db.query(Endereco).filter(Endereco.id == endereco_id).first()


def atualizar_endereco(db: Session, endereco_id: int, dados: EnderecoUpdate):
    endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
    if endereco:
        for campo, valor in dados.dict().items():
            setattr(endereco, campo, valor)
        db.commit()
        db.refresh(endereco)
    return endereco

def inativar_endereco(db: Session, endereco_id: int):
    endereco = db.query(Endereco).filter(Endereco.id == endereco_id, Endereco.ativo == True).first()
    if endereco:
        endereco.ativo = False
        db.commit()
        db.refresh(endereco)
    return endereco

def deletar_endereco(db: Session, endereco_id: int):
    endereco = db.query(Endereco).filter(Endereco.id == endereco_id).first()
    if endereco:
        db.delete(endereco)
        db.commit()
    return endereco
