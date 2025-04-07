from sqlalchemy.orm import Session
from app.models.produto_imagem import ProdutoImagem
from app.schemas.produto_imagem import ProdutoImagemCreate


def adicionar_imagem(db: Session, imagem: ProdutoImagemCreate) -> ProdutoImagem:
    nova_imagem = ProdutoImagem(**imagem.dict())
    db.add(nova_imagem)
    db.commit()
    db.refresh(nova_imagem)
    return nova_imagem


def listar_imagens(db: Session, produto_id: int):
    return db.query(ProdutoImagem).filter(ProdutoImagem.produto_id == produto_id).order_by(ProdutoImagem.ordem).all()


def remover_imagem(db: Session, imagem_id: int) -> bool:
    imagem = db.query(ProdutoImagem).filter(ProdutoImagem.id == imagem_id).first()
    if not imagem:
        return False
    db.delete(imagem)
    db.commit()
    return True
