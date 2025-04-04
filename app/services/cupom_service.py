from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.cupom import Cupom
from app.schemas.cupom_schema import CupomCreate, CupomUpdate


def criar_cupom(db: Session, cupom_data: CupomCreate):
    """ Adiciona um novo cupom ao banco de dados """
    cupom = Cupom(**cupom_data.dict())
    db.add(cupom)
    db.commit()
    db.refresh(cupom)
    return cupom


def atualizar_cupom_por_id(db: Session, cupom_id: int, cupom_data: CupomUpdate):
    """ Atualiza um cupom pelo ID """
    cupom = db.query(Cupom).filter(Cupom.id == cupom_id).first()
    if not cupom:
        return None

    for key, value in cupom_data.dict(exclude_unset=True).items():
        setattr(cupom, key, value)

    db.commit()
    db.refresh(cupom)
    return cupom

def atualizar_cupom_por_codigo(db: Session, codigo: str, cupom_data: CupomUpdate):
    """ Atualiza um cupom pelo Código """
    cupom = db.query(Cupom).filter(Cupom.codigo == codigo).first()
    if not cupom:
        return None

    for key, value in cupom_data.dict(exclude_unset=True).items():
        setattr(cupom, key, value)

    db.commit()
    db.refresh(cupom)
    return cupom


def listar_cupons(db: Session):
    cupons = db.query(Cupom).filter(Cupom.ativo == True).all()
    return cupons

def buscar_cupom_por_codigo(db: Session, codigo: str):
    cupons = db.query(Cupom).filter(Cupom.ativo == True).all()
    return cupons
def desativar_cupom(db: Session, cupom_id: int):
    """ Alterna o status de um cupom entre ativo e inativo """
    cupom = db.query(Cupom).filter(Cupom.id == cupom_id).first()
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")

    cupom.ativo = not cupom.ativo  # Alterna entre True e False
    db.commit()
    db.refresh(cupom)
    return cupom
