"""create fighter table

Revision ID: 5b7e86d6eb1c
Revises: 
Create Date: 2024-12-28 13:19:28.604742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b7e86d6eb1c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "fighter",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('age', sa.Integer, nullable=False),
        sa.Column('country', sa.String(50), nullable=False),
        sa.Column('record', sa.String(20), nullable=False),
        sa.Column('victories', sa.Integer, nullable=True, default=0),
        sa.Column('defeats', sa.Integer, nullable=True, default=0),
        sa.Column('draws', sa.Integer, nullable=True, default=0),
        sa.Column('no_contests', sa.Integer, nullable=True, default=0),
        sa.Column('image', sa.String(200), nullable=True)
    )

def downgrade() -> None:
    sa.drop_table('fighter')