"""Add the leftover columns to post

Revision ID: 97380756ba56
Revises: 56deb43078c9
Create Date: 2026-04-23 15:10:39.365751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97380756ba56'
down_revision: Union[str, Sequence[str], None] = '56deb43078c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade()-> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade()-> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass