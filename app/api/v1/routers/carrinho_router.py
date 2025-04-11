from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import carrinho_schema as schemas
from app.services import carrinho_service

router = APIRouter(prefix="/carrinho", tags=["Carrinho"])


@router.post("/adicionar", response_model=schemas.CarrinhoOut)
def adicionar_item(item: schemas.ItemCarrinhoBase, usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.adicionar_item_ao_carrinho(db, usuario_id, item)


@router.get("/", response_model=schemas.CarrinhoOut)
def ver_carrinho(usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.ver_carrinho(db, usuario_id)


@router.delete("/remover/{produto_id}", response_model=schemas.CarrinhoOut)
def remover_item(produto_id: int, usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.remover_item_do_carrinho(db, usuario_id, produto_id)


@router.put("/atualizar/{produto_id}", response_model=schemas.CarrinhoOut)
def atualizar_quantidade(produto_id: int, quantidade: int, usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.atualizar_quantidade_item(db, usuario_id, produto_id, quantidade)


@router.delete("/limpar", response_model=schemas.CarrinhoOut)
def limpar_carrinho(usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.limpar_carrinho(db, usuario_id)


@router.post("/finalizar", response_model=schemas.CarrinhoOut)
def finalizar_carrinho(usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.finalizar_carrinho(db, usuario_id)


@router.get("/historico", response_model=list[schemas.CarrinhoOut])
def listar_historico(usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.listar_carrinhos_finalizados(db, usuario_id)


@router.get("/item/{produto_id}", response_model=schemas.ItemCarrinhoOut)
def ver_item_carrinho(produto_id: int, usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.buscar_item_do_carrinho(db, usuario_id, produto_id)
