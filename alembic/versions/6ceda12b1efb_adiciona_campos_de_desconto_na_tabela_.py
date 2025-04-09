from alembic import op
import sqlalchemy as sa

# Revisões padrão
revision = 'xxxxxxxxxxxx'  # Substitua pelo ID real da revisão
down_revision = '13b20b3cb6d0'
branch_labels = None
depends_on = None

# Define o Enum fora da função para reutilização
tipo_desconto_enum = sa.Enum('cupom', 'promocao', 'nenhum', name='tipodescontoenum')

def upgrade():
    # Cria o tipo enum explicitamente
    tipo_desconto_enum.create(op.get_bind(), checkfirst=True)

    # Adiciona colunas à tabela
    op.add_column('venda', sa.Column('valor_total_bruto', sa.DECIMAL(10, 2), nullable=False, server_default="0.00"))
    op.add_column('venda', sa.Column('valor_desconto', sa.DECIMAL(10, 2), nullable=False, server_default="0.00"))
    op.add_column('venda', sa.Column('tipo_desconto', tipo_desconto_enum, nullable=False, server_default="nenhum"))

def downgrade():
    # Remove colunas
    op.drop_column('venda', 'valor_total_bruto')
    op.drop_column('venda', 'valor_desconto')
    op.drop_column('venda', 'tipo_desconto')

    # Remove o tipo enum do banco
    tipo_desconto_enum.drop(op.get_bind(), checkfirst=True)
