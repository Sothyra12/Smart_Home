"""alter devices table and add device_consumptions

Revision ID: 99a7451bc1e5
Revises: 70da2f7d045d
Create Date: 2024-07-23 14:38:34.361094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99a7451bc1e5'
down_revision: Union[str, None] = '70da2f7d045d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
 # Add new columns to devices table
    op.add_column('devices', sa.Column('is_on', sa.Boolean(), nullable=True))
    op.add_column('devices', sa.Column('power_rating', sa.Float(), nullable=True))
    op.add_column('devices', sa.Column('last_updated', sa.DateTime(), nullable=True))
    op.add_column('devices', sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False))
    op.add_column('devices', sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False))

    # Create device_consumption table
    op.create_table('device_consumption',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('consumption', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_device_consumption_id'), 'device_consumption', ['id'], unique=False)

def downgrade() -> None:
    # Drop device_consumption table
    op.drop_index(op.f('ix_device_consumption_id'), table_name='device_consumption')
    op.drop_table('device_consumption')

    # Remove new columns from devices table
    op.drop_column('devices', 'is_on')
    op.drop_column('devices', 'power_rating')
    op.drop_column('devices', 'last_updated')
    op.drop_column('devices', 'created_at')
    op.drop_column('devices', 'updated_at')
