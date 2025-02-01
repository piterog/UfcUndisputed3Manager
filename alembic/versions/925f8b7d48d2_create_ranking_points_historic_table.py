"""create ranking_points_historic table

Revision ID: 925f8b7d48d2
Revises: f307f17d3a74
Create Date: 2025-01-04 21:39:00.993320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '925f8b7d48d2'
down_revision: Union[str, None] = 'f307f17d3a74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ranking_points_historic",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('points', sa.Integer, nullable=False),
        sa.Column('model_type', sa.String(20), nullable=False),
        sa.Column('model_id', sa.Integer, nullable=False),
        sa.Column('fighter_id', sa.Integer, nullable=False),
        sa.Column('category_id', sa.Integer, nullable=False),

        sa.ForeignKeyConstraint(['fighter_id'], ['fighter.id']),
        sa.ForeignKeyConstraint(['category_id'], ['category.id']),
    )
    pass


def downgrade() -> None:
    op.drop_table('ranking_points_historic')
    pass
