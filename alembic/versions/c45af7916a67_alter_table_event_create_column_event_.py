"""alter table event create column event_completed_at

Revision ID: c45af7916a67
Revises: 16837c5c2cb4
Create Date: 2025-01-02 13:43:27.741099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c45af7916a67'
down_revision: Union[str, None] = '16837c5c2cb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('event', sa.Column('event_completed_at', sa.DateTime, nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('event', 'event_completed_at')
    pass
