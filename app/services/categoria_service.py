from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.models.produto import Produto  # Importar o modelo Produto
from app.schemas.categoria_schema import CategoriaCreate, CategoriaUpdate


def criar_categoria(db: Session, categoria: CategoriaCreate):
    # Verifica se já existe uma categoria com o mesmo nome
    categoria_existente = db.query(Categoria).filter(Categoria.nome == categoria.nome).first()

    if categoria_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria com esse nome já existe"
        )

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


# Função para listar categorias ativas
def listar_categorias(db: Session):
    return db.query(Categoria).filter(Categoria.ativo == True).all()


# Função para buscar uma categoria por ID
def buscar_categoria(db: Session, categoria_id: int):
    return db.query(Categoria).filter(Categoria.id == categoria_id, Categoria.ativo == True).first()


def atualizar_categoria(db: Session, categoria_id: int, categoria_dados: CategoriaUpdate):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        return None  # Retorna None para indicar que não encontrou a categoria

    # Atualizando os campos fornecidos
    for key, value in categoria_dados.dict(exclude_unset=True).items():
        setattr(categoria, key, value)

    db.commit()
    db.refresh(categoria)
    return categoria


def inativar_categoria_e_atualizar_produtos(db: Session, categoria_id: int):
    try:
        # Recupera a categoria a ser inativada
        categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()

        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")

        # Marcar a categoria como inativa
        categoria.ativo = False
        db.commit()

        # Buscar a categoria padrão (não atribuída)
        categoria_padrao = db.query(Categoria).filter(Categoria.nome == "Categoria Não Atribuída").first()

        if not categoria_padrao:
            # Criar categoria padrão se não existir
            categoria_padrao = Categoria(
                nome="Categoria Não Atribuída",
                descricao="Categoria padrão para produtos sem categoria válida",
                ativo=True
            )
            db.add(categoria_padrao)
            db.commit()
            db.refresh(categoria_padrao)

        # Atualizar os produtos relacionados à categoria inativa
        produtos = db.query(Produto).filter(Produto.categoria_id == categoria_id).all()

        for produto in produtos:
            produto.categoria_id = categoria_padrao.id  # Atribui a categoria padrão aos produtos
            db.add(produto)

        db.commit()

        return {"detail": "Categoria inativada e produtos atualizados para a categoria padrão."}

    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao inativar categoria e atualizar produtos: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao inativar categoria e atualizar produtos"
        )

