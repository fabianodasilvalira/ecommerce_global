from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate

def criar_categoria(db: Session, categoria: CategoriaCreate):
    nova_categoria = Categoria(
        nome=categoria.nome,
        descricao=categoria.descricao,
        imagem_url=categoria.imagem_url,
        cor_destaque=categoria.cor_destaque,
        ativo=categoria.ativo
    )
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria

def listar_categorias(db: Session):
    return db.query(Categoria).filter(Categoria.ativo == True).all()

def buscar_categoria(db: Session, categoria_id: int):
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()


def atualizar_categoria(db: Session, categoria_id: int, categoria_dados: CategoriaUpdate):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        return None  # Retorna None para indicar que não encontrou a categoria

    if not categoria_dados:
        return categoria  # Se não há mudanças, retorna a categoria original

    for key, value in categoria_dados.dict(exclude_unset=True).items():
        setattr(categoria, key, value)

    db.commit()
    db.refresh(categoria)
    return categoria


def deletar_categoria(db: Session, categoria_id: int):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if categoria:
        db.delete(categoria)
        db.commit()
    return categoria