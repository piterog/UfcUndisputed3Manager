"""create category fighter table

Revision ID: 45543d38e699
Revises: 66d43850654c
Create Date: 2024-12-28 13:32:54.217257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45543d38e699'
down_revision: Union[str, None] = '66d43850654c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "category_fighter",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('fighter_id', sa.Integer, nullable=False),
        sa.Column('category_id', sa.Integer, nullable=False),
        sa.Column('ranking', sa.Integer, nullable=False),

        sa.ForeignKeyConstraint(['fighter_id'], ['fighter.id']),
        sa.ForeignKeyConstraint(['category_id'], ['category.id']),
    )

def downgrade() -> None:
    sa.drop_table('category_fighter')