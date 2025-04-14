from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.categoria_imagem import CategoriaImagem
from app.models.categoria import Categoria
from app.schemas.categoria_imagem_schema import CategoriaImagemCreate, CategoriaImagemReorder
from fastapi import HTTPException

def criar_categoria_imagem(db: Session, imagem_data: CategoriaImagemCreate):
    # Verifica se categoria existe
    categoria = db.query(Categoria).filter(Categoria.id == imagem_data.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    # Verifica se já existe uma imagem do mesmo tipo e ordem para essa categoria
    imagem_existente = db.query(CategoriaImagem).filter_by(
        categoria_id=imagem_data.categoria_id,
        tipo=imagem_data.tipo,
        ordem=imagem_data.ordem
    ).first()

    if imagem_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe uma imagem com esse tipo e ordem para a categoria"
        )

    # Convertendo a URL de HttpUrl para string
    imagem_data.imagem_url = str(imagem_data.imagem_url)

    # Criação do novo objeto CategoriaImagem
    nova_imagem = CategoriaImagem(**imagem_data.dict())
    db.add(nova_imagem)
    db.commit()
    db.refresh(nova_imagem)
    return nova_imagem


def listar_imagens_por_categoria(db: Session, categoria_id: int):
    return db.query(CategoriaImagem)\
             .filter(CategoriaImagem.categoria_id == categoria_id)\
             .order_by(CategoriaImagem.ordem)\
             .all()


def buscar_imagem(db: Session, imagem_id: int):
    return db.query(CategoriaImagem).filter(CategoriaImagem.id == imagem_id).first()


def deletar_imagem(db: Session, imagem_id: int):
    imagem = buscar_imagem(db, imagem_id)
    if imagem:
        db.delete(imagem)
        db.commit()
    return imagem


def reordenar_imagens(db: Session, ordens: list[CategoriaImagemReorder]):
    for item in ordens:
        imagem = db.query(CategoriaImagem).filter_by(id=item.id).first()
        if imagem:
            imagem.ordem = item.nova_ordem
    db.commit()
