"""create ranking_history table

Revision ID: 15d6c05c7104
Revises: 925f8b7d48d2
Create Date: 2025-01-10 14:01:12.306134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15d6c05c7104'
down_revision: Union[str, None] = '925f8b7d48d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ranking_history",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('event_id', sa.Integer, nullable=False),
        sa.Column('fighter_id', sa.Integer, nullable=False),
        sa.Column('category_id', sa.Integer, nullable=False),
        sa.Column('order', sa.Integer, nullable=False),

        sa.ForeignKeyConstraint(['event_id'], ['event.id']),
        sa.ForeignKeyConstraint(['category_id'], ['category.id']),
        sa.ForeignKeyConstraint(['fighter_id'], ['fighter.id']),
    )


def downgrade() -> None:
    sa.drop_table('ranking_history')
