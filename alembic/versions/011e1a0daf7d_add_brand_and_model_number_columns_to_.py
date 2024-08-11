"""Add brand and model_number columns to devices table

Revision ID: 011e1a0daf7d
Revises: 99a7451bc1e5
Create Date: 2024-08-10 09:58:03.069232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '011e1a0daf7d'
down_revision: Union[str, None] = '99a7451bc1e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('devices', sa.Column('brand', sa.String(length=100), nullable=True))
    op.add_column('devices', sa.Column('model_number', sa.String(length=100), nullable=True))



def downgrade() -> None:    
    op.drop_column('devices', 'brand')
    op.drop_column('devices', 'model_number')
