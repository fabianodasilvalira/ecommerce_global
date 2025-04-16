from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.carrinho_schema import CarrinhoAtualizarInput
from app.schemas.venda_schema import VendaResponse  # 👈 adicione isso

from app.db.database import get_db
from app.schemas import carrinho_schema as schemas
from app.services import carrinho_service
from app.services import venda_service as service_venda
from app.models import Usuario


router = APIRouter()


@router.post("/adicionar", response_model=schemas.CarrinhoOut)
def adicionar_item(item: schemas.ItemCarrinhoBase, usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.adicionar_item_ao_carrinho(db, usuario_id, item)


@router.get("/", response_model=schemas.CarrinhoOut)
def ver_carrinho(usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.ver_carrinho(db, usuario_id)


@router.delete("/remover/{produto_id}", response_model=schemas.CarrinhoOut)
def remover_item(produto_id: int, usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.remover_item_do_carrinho(db, usuario_id, produto_id)


@router.put("/atualizar/{produto_id}/produto", response_model=schemas.CarrinhoOut)
def atualizar_quantidade(
        produto_id: int,
        dados: CarrinhoAtualizarInput,  # Recebe dados no corpo da requisição (JSON)
        db: Session = Depends(get_db)
):
    usuario_id = dados.usuario_id  # Obtém o usuario_id do corpo da requisição
    quantidade = dados.itens[
        0].quantidade  # Aqui, pegamos a quantidade do primeiro item (poderia ter lógica para múltiplos itens)

    # Chama o serviço que trata a lógica de atualizar o carrinho
    return carrinho_service.atualizar_quantidade_item(db, usuario_id, produto_id, quantidade)


@router.delete("/limpar", response_model=schemas.CarrinhoOut)
def limpar_carrinho(usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.limpar_carrinho(db, usuario_id)

@router.post("/finalizar-e-criar-venda", response_model=VendaResponse)
def finalizar_e_criar_venda_a_partir_do_carrinho(
    usuario_id: int,
    endereco_id: int,
    cupom_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    venda = service_venda.criar_venda_a_partir_do_carrinho(
        db=db,
        usuario=usuario,
        endereco_id=endereco_id,
        cupom_id=cupom_id
    )
    return venda


@router.post("/finalizar", response_model=VendaResponse)
def finalizar_carrinho(
        usuario_id: int,
        endereco_id: int,
        cupom_id: Optional[int] = None,
        db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).get(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return carrinho_service.finalizar_carrinho_e_criar_venda(
        db=db,
        usuario_id=usuario_id,
        endereco_id=endereco_id,
        cupom_id=cupom_id
    )

@router.get("/historico", response_model=list[schemas.CarrinhoOut])
def listar_historico(usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.listar_carrinhos_finalizados(db, usuario_id)


@router.get("/item/{produto_id}", response_model=schemas.ItemCarrinhoOut)
def ver_item_carrinho(produto_id: int, usuario_id: int, db: Session = Depends(get_db)):
    return carrinho_service.ver_item_especifico(db, usuario_id, produto_id)


@router.get("/finalizados", response_model=List[schemas.CarrinhoOut])
def listar_carrinhos_finalizados(
        usuario_id: int = Query(..., description="ID do usuário"),
        skip: int = Query(0, description="Pular registros"),
        limit: int = Query(100, description="Limite de registros por página"),
        db: Session = Depends(get_db)
):
    """
    Lista todos os carrinhos finalizados de um usuário específico.

    Parâmetros:
    - usuario_id: ID do usuário (obrigatório)
    - skip: Número de registros para pular (para paginação)
    - limit: Número máximo de registros por página (padrão 100)
    """
    return carrinho_service.listar_carrinhos_finalizados(db, usuario_id, skip, limit)
