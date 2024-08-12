"""Create user settings table

Revision ID: c7f72b88284e
Revises: e01ad4b754ad
Create Date: 2024-08-11 21:13:25.919794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'c7f72b88284e'
down_revision: Union[str, None] = 'e01ad4b754ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'user_settings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id'), nullable=False),
        sa.Column('setting_key', sa.String(length=50), nullable=False),
        sa.Column('setting_value', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
    )

def downgrade():
    op.drop_table('user_settings')