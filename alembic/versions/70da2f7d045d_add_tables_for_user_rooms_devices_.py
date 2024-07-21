"""add tables for user rooms, devices, configuration, profile and user settings

Revision ID: 70da2f7d045d
Revises: ffd146685594
Create Date: 2024-07-21 09:28:41.094874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70da2f7d045d'
down_revision: Union[str, None] = 'ffd146685594'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
