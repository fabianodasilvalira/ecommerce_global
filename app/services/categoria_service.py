from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.models.produto import Produto
from app.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate
import logging

logger = logging.getLogger(__name__)


def criar_categoria(db: Session, categoria: CategoriaCreate):
    # Verifica se já existe uma categoria com o mesmo nome ou slug
    categoria_existente = db.query(Categoria).filter(
        (Categoria.nome == categoria.nome) |
        (Categoria.slug == categoria.slug)
    ).first()

    if categoria_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria com esse nome ou slug já existe"
        )

    nova_categoria = Categoria(**categoria.model_dump())
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria


def listar_categorias(db: Session, incluir_inativas: bool = False):
    query = db.query(Categoria)
    if not incluir_inativas:
        query = query.filter(Categoria.ativo == True)

    categorias = query.order_by(Categoria.ordem).all()

    # Adiciona contagem de produtos
    for cat in categorias:
        cat.produtos_count = db.query(Produto).filter(
            Produto.categoria_id == cat.id,
            Produto.ativo == True
        ).count()

    return categorias


def buscar_categoria(db: Session, categoria_id: int):
    categoria = db.query(Categoria).get(categoria_id)
    if categoria:
        categoria.produtos_count = db.query(Produto).filter(
            Produto.categoria_id == categoria.id,
            Produto.ativo == True
        ).count()
    return categoria


def atualizar_categoria(db: Session, categoria_id: int, categoria_dados: CategoriaUpdate):
    categoria = db.query(Categoria).get(categoria_id)
    if not categoria:
        return None

    update_data = categoria_dados.model_dump(exclude_unset=True)

    # Verifica se o novo slug já existe
    if 'slug' in update_data:
        slug_existente = db.query(Categoria).filter(
            Categoria.slug == update_data['slug'],
            Categoria.id != categoria_id
        ).first()
        if slug_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma categoria com este slug"
            )

    for key, value in update_data.items():
        setattr(categoria, key, value)

    db.commit()
    db.refresh(categoria)
    return categoria


def inativar_categoria_e_atualizar_produtos(db: Session, categoria_id: int):
    try:
        db.begin()

        categoria = db.query(Categoria).get(categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

        categoria.ativo = False

        # Buscar ou criar categoria padrão
        categoria_padrao = db.query(Categoria).filter(
            Categoria.nome == "Sem Categoria",
            Categoria.slug == "sem-categoria"
        ).first()

        if not categoria_padrao:
            categoria_padrao = Categoria(
                nome="Sem Categoria",
                slug="sem-categoria",
                descricao="Produtos sem categoria atribuída",
                ativo=True
            )
            db.add(categoria_padrao)
            db.commit()
            db.refresh(categoria_padrao)

        # Atualizar produtos
        db.query(Produto).filter(
            Produto.categoria_id == categoria_id
        ).update({"categoria_id": categoria_padrao.id})

        db.commit()
        return categoria

    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao inativar categoria: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao processar inativação da categoria"
        )