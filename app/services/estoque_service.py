from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.estoque import Estoque
from app.models.produto import Produto
from app.schemas.estoque import EstoqueCreate, EstoqueUpdate

def adicionar_estoque(db: Session, estoque_data: EstoqueCreate):
    """ Adiciona ou atualiza o estoque de um produto """
    produto = db.query(Produto).filter(Produto.id == estoque_data.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    estoque = db.query(Estoque).filter(Estoque.produto_id == estoque_data.produto_id).first()

    if estoque:
        estoque.quantidade += estoque_data.quantidade
    else:
        estoque = Estoque(
            produto_id=estoque_data.produto_id,
            quantidade=estoque_data.quantidade
        )
        db.add(estoque)

    db.commit()
    db.refresh(estoque)
    return estoque

def obter_estoque(db: Session, produto_id: int):
    """ Retorna a quantidade disponível no estoque de um produto """
    estoque = db.query(Estoque).filter(Estoque.produto_id == produto_id).first()
    if not estoque:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    return estoque

def listar_estoque(db: Session):
    """ Retorna todos os itens do estoque """
    return db.query(Estoque).all()

def atualizar_estoque(db: Session, produto_id: int, estoque_data: EstoqueUpdate):
    """ Atualiza a quantidade de um item no estoque """
    estoque = db.query(Estoque).filter(Estoque.produto_id == produto_id).first()
    if not estoque:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")

    estoque.quantidade = estoque_data.quantidade
    db.commit()
    db.refresh(estoque)
    return estoque

def deletar_estoque(db: Session, produto_id: int):
    """ Remove um item do estoque """
    estoque = db.query(Estoque).filter(Estoque.produto_id == produto_id).first()
    if not estoque:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")

    db.delete(estoque)
    db.commit()
    return {"message": "Estoque removido com sucesso"}
