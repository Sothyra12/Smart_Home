"""Add user type column to users table

Revision ID: e01ad4b754ad
Revises: 964d6eb88a89
Create Date: 2024-08-11 16:34:38.100765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e01ad4b754ad'
down_revision: Union[str, None] = '964d6eb88a89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create an ENUM type for user types
    user_types = ['Tech Enthusiast', 'Remote Manager', 'Eco-Conscious User', 'Family Oriented', 'Administrator']
    user_type_enum = sa.Enum(*user_types, name='user_types')
    
    # Add the column with the ENUM type
    op.add_column('users', sa.Column('user_type', user_type_enum, nullable=True))

def downgrade():
    op.drop_column('users', 'user_type')
    op.execute('DROP TYPE user_types')
