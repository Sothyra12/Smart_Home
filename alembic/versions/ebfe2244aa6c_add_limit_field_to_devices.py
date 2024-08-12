"""Add limit field to devices

Revision ID: ebfe2244aa6c
Revises: c7f72b88284e
Create Date: 2024-08-11 21:15:03.290313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebfe2244aa6c'
down_revision: Union[str, None] = 'c7f72b88284e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('devices', sa.Column('energy_limit', sa.Float, nullable=True))

def downgrade():
    op.drop_column('devices', 'energy_limit')