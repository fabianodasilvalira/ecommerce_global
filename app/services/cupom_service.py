from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.cupom import Cupom
from app.schemas.cupom_schema import CupomCreate, CupomUpdate, CupomResponse


def criar_cupom(db: Session, cupom_data: CupomCreate) -> CupomResponse:
    cupom = Cupom(**cupom_data.dict())
    db.add(cupom)
    db.commit()
    db.refresh(cupom)
    return CupomResponse.model_validate(cupom)


def atualizar_cupom_por_id(db: Session, cupom_id: int, cupom_data: CupomUpdate) -> CupomResponse | None:
    cupom = db.query(Cupom).filter(Cupom.id == cupom_id).first()
    if not cupom:
        return None

    for key, value in cupom_data.dict(exclude_unset=True).items():
        setattr(cupom, key, value)

    db.commit()
    db.refresh(cupom)
    return CupomResponse.model_validate(cupom)


def atualizar_cupom_por_codigo(db: Session, codigo: str, cupom_data: CupomUpdate) -> CupomResponse | None:
    cupom = db.query(Cupom).filter(Cupom.codigo == codigo).first()
    if not cupom:
        return None

    for key, value in cupom_data.dict(exclude_unset=True).items():
        setattr(cupom, key, value)

    db.commit()
    db.refresh(cupom)
    return CupomResponse.model_validate(cupom)


def listar_cupons(db: Session) -> list[CupomResponse]:
    cupons = db.query(Cupom).filter(Cupom.ativo == True).all()
    return [CupomResponse.model_validate(c) for c in cupons]


def buscar_cupom_por_codigo(db: Session, codigo: str) -> CupomResponse | None:
    cupom = db.query(Cupom).filter(Cupom.codigo == codigo, Cupom.ativo == True).first()
    if not cupom:
        return None
    return CupomResponse.model_validate(cupom)


def desativar_cupom(db: Session, cupom_id: int) -> CupomResponse | None:
    cupom = db.query(Cupom).filter(Cupom.id == cupom_id).first()
    if not cupom:
        return None

    cupom.ativo = not cupom.ativo
    db.commit()
    db.refresh(cupom)
    return CupomResponse.model_validate(cupom)
