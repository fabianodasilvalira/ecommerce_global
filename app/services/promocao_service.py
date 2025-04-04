from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.promocao import Promocao
from app.models.produto import Produto
from app.schemas.promocao_schema import PromocaoCreate, PromocaoUpdate
from datetime import datetime

def criar_promocao_service(db: Session, promocao_data: PromocaoCreate):
    # Verifica se já existe uma promoção ativa para este produto no mesmo período
    promocao_existente = db.query(Promocao).filter(
        Promocao.produto_id == promocao_data.produto_id,
        Promocao.ativo == True,
        Promocao.data_inicio <= promocao_data.data_fim,  # A nova promoção não pode começar antes do fim da existente
        Promocao.data_fim >= promocao_data.data_inicio   # A nova promoção não pode terminar depois do início da existente
    ).first()

    if promocao_existente:
        raise HTTPException(status_code=400, detail="Já existe uma promoção ativa para este produto no período informado")

    # Criar nova promoção
    nova_promocao = Promocao(**promocao_data.dict())
    db.add(nova_promocao)
    db.commit()
    db.refresh(nova_promocao)

    return nova_promocao


def listar_promocoes_ativas_service(db: Session):
    return db.query(Promocao).filter(Promocao.ativo == True, Promocao.data_fim >= datetime.utcnow()).all()

def buscar_promocao_service(db: Session, promocao_id: int):
    promocao = db.query(Promocao).filter(
        Promocao.id == promocao_id,
        Promocao.ativo == True  # Apenas promoções ativas
    ).first()

    if not promocao:
        raise HTTPException(status_code=404, detail="Promoção não encontrada ou inativa")

    return promocao

def editar_promocao_service(db: Session, promocao_id: int, update_data: PromocaoUpdate):
    promocao = db.query(Promocao).filter(Promocao.id == promocao_id).first()
    if not promocao:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")

    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(promocao, field, value)

    db.commit()
    db.refresh(promocao)
    return promocao

def inativar_promocao_service(db: Session, promocao_id: int):
    promocao = db.query(Promocao).filter(Promocao.id == promocao_id).first()
    if not promocao:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")

    promocao.ativo = not promocao.ativo

    db.commit()
    db.refresh(promocao)
    return promocao
