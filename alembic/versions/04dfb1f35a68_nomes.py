"""nomes

Revision ID: 04dfb1f35a68
Revises: 
Create Date: 2024-01-11 22:44:53.577402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04dfb1f35a68'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('nomes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(length=80), nullable=False, unique=True),
    )


def downgrade():
    op.drop_table('nomes')
