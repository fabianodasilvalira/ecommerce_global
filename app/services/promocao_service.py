from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.promocao import Promocao
from app.schemas.promocao_schema import PromocaoCreate, PromocaoUpdate

def criar_promocao_service(db: Session, promocao_data: PromocaoCreate):
    # Validação de sobreposição de período
    promocao_existente = db.query(Promocao).filter(
        Promocao.produto_id == promocao_data.produto_id,
        Promocao.ativo == True,
        Promocao.data_inicio <= promocao_data.data_fim,
        Promocao.data_fim >= promocao_data.data_inicio
    ).first()

    if promocao_existente:
        raise HTTPException(status_code=400, detail="Já existe uma promoção ativa para este produto no período informado")

    nova_promocao = Promocao(**promocao_data.dict())
    db.add(nova_promocao)
    db.commit()
    db.refresh(nova_promocao)
    return nova_promocao

def listar_promocoes_ativas_service(db: Session):
    agora = datetime.utcnow()
    return db.query(Promocao).filter(
        Promocao.ativo == True,
        Promocao.data_inicio <= agora,
        Promocao.data_fim >= agora
    ).all()

def buscar_promocao_service(db: Session, promocao_id: int):
    promocao = db.query(Promocao).filter(
        Promocao.id == promocao_id,
        Promocao.ativo == True
    ).first()

    if not promocao:
        raise HTTPException(status_code=404, detail="Promoção não encontrada ou inativa")

    return promocao

def editar_promocao_service(db: Session, promocao_id: int, update_data: PromocaoUpdate):
    promocao = db.query(Promocao).filter(Promocao.id == promocao_id).first()
    if not promocao:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(promocao, field, value)

    db.commit()
    db.refresh(promocao)
    return promocao

def inativar_promocao_service(db: Session, promocao_id: int):
    promocao = db.query(Promocao).filter(Promocao.id == promocao_id).first()
    if not promocao:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")

    promocao.ativo = False
    db.commit()
    db.refresh(promocao)
    return promocao
