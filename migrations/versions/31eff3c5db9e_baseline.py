"""baseline

Revision ID: 31eff3c5db9e
Revises: 
Create Date: 2026-10-20 14:35:39.744570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31eff3c5db9e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        CREATE TABLE tasks (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


def downgrade():
    op.execute("""
        DROP TABLE tasks
    """)
