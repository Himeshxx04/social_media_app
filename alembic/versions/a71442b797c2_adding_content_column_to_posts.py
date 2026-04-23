"""adding content column to posts

Revision ID: a71442b797c2
Revises: aa8fef58e2b6
Create Date: 2026-04-23 13:46:58.633017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a71442b797c2'
down_revision: Union[str, Sequence[str], None] = 'aa8fef58e2b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
