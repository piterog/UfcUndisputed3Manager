"""alter table fight create column save_fight_at

Revision ID: 16837c5c2cb4
Revises: 37b25df2af22
Create Date: 2025-01-02 13:40:36.038479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16837c5c2cb4'
down_revision: Union[str, None] = '37b25df2af22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('fight', sa.Column('save_fight_at', sa.DateTime, nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('fight', 'save_fight_at')
    pass
