from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context

# Importando a Base e o engine corretamente
from app.db.database import engine, Base  # Certifique-se de que está correto
from app.models import usuario  # Inclui o modelo para garantir que o Alembic reconheça as tabelas

# Configuração do Alembic
config = context.config

# Configuração de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados do banco para autogeração
from app.db.database import Base
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.produto_imagem import ProdutoImagem
from app.models.promocao import Promocao
from app.models.estoque import Estoque
from app.models.movimentacao_estoque import MovimentacaoEstoque
from app.models.venda import Venda
from app.models.pagamento import Pagamento
from app.models.itemVenda import ItemVenda
from app.models.entrega import Entrega
from app.models.rastreamento_entrega import RastreamentoEntrega
from app.models.cupom import Cupom
from app.models.endereco import Endereco

target_metadata = Base.metadata



def run_migrations_offline() -> None:
    """Executa as migrações no modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrações no modo online."""
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
