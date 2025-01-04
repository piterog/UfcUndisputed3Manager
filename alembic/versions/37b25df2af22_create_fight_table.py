"""create fight table

Revision ID: 37b25df2af22
Revises: 1ef216bc1a40
Create Date: 2024-12-28 13:52:23.389966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37b25df2af22'
down_revision: Union[str, None] = '1ef216bc1a40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "fight",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('number', sa.Integer, nullable=True),
        sa.Column('event_id', sa.Integer, nullable=False),
        sa.Column('category_id', sa.Integer, nullable=False),
        sa.Column('red_corner_id', sa.Integer),
        sa.Column('blue_corner_id', sa.Integer),
        sa.Column('control', sa.Integer, nullable=True),
        sa.Column('belt_dispute', sa.Boolean, default=False),
        sa.Column('winner_id', sa.Integer, nullable=True),
        sa.Column('loser_id', sa.Integer, nullable=True),
        sa.Column('method', sa.String(50), nullable=True),
        sa.Column('round', sa.Integer, nullable=True),
        sa.Column('time', sa.Time, nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),

        sa.ForeignKeyConstraint(['event_id'], ['event.id']),
        sa.ForeignKeyConstraint(['category_id'], ['category.id']),
        sa.ForeignKeyConstraint(['red_corner_id'], ['fighter.id']),
        sa.ForeignKeyConstraint(['blue_corner_id'], ['fighter.id']),
        sa.ForeignKeyConstraint(['winner_id'], ['fighter.id']),
        sa.ForeignKeyConstraint(['loser_id'], ['fighter.id']),
    )

def downgrade() -> None:
    sa.drop_table('fight')
