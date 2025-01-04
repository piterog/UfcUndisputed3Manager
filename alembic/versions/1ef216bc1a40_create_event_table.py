"""create event table

Revision ID: 1ef216bc1a40
Revises: 45543d38e699
Create Date: 2024-12-28 13:50:24.798605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ef216bc1a40'
down_revision: Union[str, None] = '45543d38e699'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "event",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String(200), unique=False, nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )

def downgrade() -> None:
    sa.drop_table('event')
