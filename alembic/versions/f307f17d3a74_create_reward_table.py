"""create reward table

Revision ID: f307f17d3a74
Revises: c45af7916a67
Create Date: 2025-01-04 17:21:31.711857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f307f17d3a74'
down_revision: Union[str, None] = 'c45af7916a67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reward",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('fighter_id', sa.Integer, nullable=False),
        sa.Column('fight_id', sa.Integer, nullable=False),
        sa.Column('event_id', sa.Integer, nullable=False),

        sa.ForeignKeyConstraint(['fighter_id'], ['fighter.id']),
        sa.ForeignKeyConstraint(['fight_id'], ['fight.id']),
        sa.ForeignKeyConstraint(['event_id'], ['event.id']),
    )

def downgrade() -> None:
    sa.drop_table('reward')