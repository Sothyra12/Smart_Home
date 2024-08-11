"""Add timestamp column to device_consumptions table

Revision ID: 964d6eb88a89
Revises: 011e1a0daf7d
Create Date: 2024-08-10 16:57:20.780068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '964d6eb88a89'
down_revision: Union[str, None] = '011e1a0daf7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('device_consumption', sa.Column('timestamp', sa.DateTime(timezone=True), server_default=func.now(), nullable=False))

def downgrade():
    op.drop_column('device_consumption', 'timestamp')
