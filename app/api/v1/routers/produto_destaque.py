from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.produto_destaque_schema import ProdutoDestaqueCreate, ProdutoDestaqueResponse, ProdutoDestaqueUpdate, ProdutoDestaqueComProduto
from app.services.produto_destaque_service import ProdutoDestaqueService

router = APIRouter()

@router.post("/", response_model=ProdutoDestaqueResponse, status_code=status.HTTP_201_CREATED)
def criar_destaque(destaque: ProdutoDestaqueCreate, db: Session = Depends(get_db)):
    service = ProdutoDestaqueService(db)
    try:
        return service.criar_destaque(destaque)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=list[ProdutoDestaqueComProduto])
def listar_destaques(tipo: str = None, ativo: bool = True, db: Session = Depends(get_db)):
    service = ProdutoDestaqueService(db)
    return service.listar_destaques(tipo, ativo)

@router.get("/{destaque_id}", response_model=ProdutoDestaqueComProduto)
def obter_destaque(destaque_id: int, db: Session = Depends(get_db)):
    service = ProdutoDestaqueService(db)
    destaque = service.obter_destaque_por_id(destaque_id)
    if not destaque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destaque não encontrado"
        )
    return destaque

@router.put("/{destaque_id}", response_model=ProdutoDestaqueResponse)
def atualizar_destaque(destaque_id: int, destaque: ProdutoDestaqueUpdate, db: Session = Depends(get_db)):
    service = ProdutoDestaqueService(db)
    db_destaque = service.atualizar_destaque(destaque_id, destaque)
    if not db_destaque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destaque não encontrado"
        )
    return db_destaque

@router.delete("/{destaque_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_destaque(destaque_id: int, db: Session = Depends(get_db)):
    service = ProdutoDestaqueService(db)
    if not service.remover_destaque(destaque_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destaque não encontrado"
        )

@router.patch("/{destaque_id}/alternar-status", response_model=ProdutoDestaqueResponse)
def alternar_status_destaque(destaque_id: int, db: Session = Depends(get_db)):
    service = ProdutoDestaqueService(db)
    db_destaque = service.alternar_status_destaque(destaque_id)
    if not db_destaque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destaque não encontrado"
        )
    return db_destaque