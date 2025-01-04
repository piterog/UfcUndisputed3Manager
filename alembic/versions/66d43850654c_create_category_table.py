"""create category table

Revision ID: 66d43850654c
Revises: 5b7e86d6eb1c
Create Date: 2024-12-28 13:32:25.797085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66d43850654c'
down_revision: Union[str, None] = '5b7e86d6eb1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "category",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String(200), unique=True),
        sa.Column('champion_id', sa.Integer(), nullable=False),

        sa.ForeignKeyConstraint(['champion_id'], ['fighter.id']),
    )

def downgrade() -> None:
    sa.drop_table('category')
