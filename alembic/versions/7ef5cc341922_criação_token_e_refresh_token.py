"""criação token e refresh token

Revision ID: 7ef5cc341922
Revises: f5587af985fb
Create Date: 2025-04-02 10:27:22.470299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ef5cc341922'
down_revision: Union[str, None] = 'f5587af985fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('refresh_token', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuario', 'refresh_token')
    # ### end Alembic commands ###
