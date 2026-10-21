"""add priority to tasks

Revision ID: 5c3b4ea14063
Revises: 31eff3c5db9e
Create Date: 2026-10-20 15:00:00.057687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c3b4ea14063'
down_revision: Union[str, Sequence[str], None] = '31eff3c5db9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
               ALTER TABLE tasks
               ADD COLUMN priority TEXT NOT NULL DEFAULT 'medium'
               """)


def downgrade() -> None:
    op.execute("""
               ALTER TABLE tasks
               DROP COLUMN priority
               """)
