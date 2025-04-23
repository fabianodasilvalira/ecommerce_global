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

    # Criar nova promoção
    try:
        nova_promocao = Promocao(**promocao_data.dict())  # Criação da promoção com os dados recebidos
        db.add(nova_promocao)
        db.commit()
        db.refresh(nova_promocao)  # Atualiza os dados da nova promoção
        return nova_promocao
    except Exception as e:
        db.rollback()  # Desfaz a transação se algo der errado
        raise HTTPException(status_code=500, detail=f"Erro ao criar promoção: {str(e)}")

def listar_promocoes_ativas_service(db: Session):
    agora = datetime.utcnow()  # Pega a data e hora atual UTC
    try:
        return db.query(Promocao).filter(
            Promocao.ativo == True,
            Promocao.data_inicio <= agora,
            Promocao.data_fim >= agora
        ).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar promoções ativas: {str(e)}")

def buscar_promocao_service(db: Session, promocao_id: int):
    try:
        promocao = db.query(Promocao).filter(
            Promocao.id == promocao_id,
            Promocao.ativo == True
        ).first()

        if not promocao:
            raise HTTPException(status_code=404, detail="Promoção não encontrada ou inativa")
        return promocao
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar promoção: {str(e)}")

def editar_promocao_service(db: Session, promocao_id: int, update_data: PromocaoUpdate):
    try:
        promocao = db.query(Promocao).filter(Promocao.id == promocao_id).first()
        if not promocao:
            raise HTTPException(status_code=404, detail="Promoção não encontrada")

        # Atualizar os campos da promoção
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(promocao, field, value)

        db.commit()  # Comitar as alterações
        db.refresh(promocao)  # Atualizar o objeto da promoção
        return promocao
    except Exception as e:
        db.rollback()  # Reverter a transação em caso de erro
        raise HTTPException(status_code=500, detail=f"Erro ao editar promoção: {str(e)}")

def inativar_promocao_service(db: Session, promocao_id: int):
    try:
        promocao = db.query(Promocao).filter(Promocao.id == promocao_id).first()
        if not promocao:
            raise HTTPException(status_code=404, detail="Promoção não encontrada")

        promocao.ativo = False  # Inativar a promoção
        db.commit()  # Comitar a alteração
        db.refresh(promocao)  # Atualizar o objeto da promoção
        return promocao
    except Exception as e:
        db.rollback()  # Reverter a transação em caso de erro
        raise HTTPException(status_code=500, detail=f"Erro ao inativar promoção: {str(e)}")
