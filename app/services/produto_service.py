from sqlalchemy.orm import Session
from app.models.produto import Produto
import random
import string


def generate_sku(nome: str, categoria: str) -> str:
    """Gera um SKU único baseado no nome, categoria e um código aleatório."""
    prefixo = nome[:3].upper() if nome else "PRD"
    categoria_prefixo = categoria[:3].upper() if categoria else "GEN"
    codigo = ''.join(random.choices(string.digits, k=4))

    return f"{prefixo}-{categoria_prefixo}-{codigo}"


def criar_produto(db: Session, nome: str, descricao: str, preco: float, categoria_id: int):
    """Cria um novo produto com SKU gerado automaticamente."""
    sku = generate_sku(nome, str(categoria_id))

    novo_produto = Produto(
        nome=nome,
        descricao=descricao,
        preco=preco,
        categoria_id=categoria_id,
        sku=sku
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto
