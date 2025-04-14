from sqlalchemy.orm import Session
from app.models.produto_imagem import ProdutoImagem  # ou onde estiver seu modelo
from app.schemas.produto_imagem_schema import ProdutoImagemCreate, ProdutoImagemUpdate
from sqlalchemy import func

def criar_imagem_produto(db: Session, dados: ProdutoImagemCreate):
    nova_imagem = ProdutoImagem(
        produto_id=dados.produto_id,
        imagem_url=str(dados.imagem_url),  # conversão aqui
        tipo=dados.tipo.value,
        ordem=dados.ordem,
        visivel=dados.visivel
    )
    db.add(nova_imagem)
    db.commit()
    db.refresh(nova_imagem)
    return nova_imagem

def editar_imagem_produto(db: Session, imagem_id: int, imagem_data: ProdutoImagemUpdate):
    imagem = buscar_imagem_produto(db, imagem_id)
    if not imagem:
        return None

    # Atualiza apenas os campos que foram informados
    for key, value in imagem_data.dict(exclude_unset=True).items():
        setattr(imagem, key, value)

    db.commit()
    db.refresh(imagem)
    return imagem


def listar_imagens_produto(db: Session, produto_id: int):
    return db.query(ProdutoImagem).filter_by(produto_id=produto_id).order_by(ProdutoImagem.ordem.asc()).all()

def buscar_imagem_produto(db: Session, imagem_id: int):
    return db.query(ProdutoImagem).filter_by(id=imagem_id).first()

def deletar_imagem_produto(db: Session, imagem_id: int):
    imagem = buscar_imagem_produto(db, imagem_id)
    if imagem:
        imagem.visivel = False
        db.commit()
        db.refresh(imagem)
    return imagem
