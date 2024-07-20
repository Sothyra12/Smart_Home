"""alter_user_table

Revision ID: ffd146685594
Revises: 69f729d2445f
Create Date: 2024-07-20 16:09:18.657828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = 'ffd146685594'
down_revision: Union[str, None] = '69f729d2445f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename 'id' to 'user_id'
    op.alter_column('users', 'id', new_column_name='user_id', existing_type=sa.Integer(), autoincrement=True, nullable=False)
    
    # Add new columns
    op.add_column('users', sa.Column('username', sa.String(length=50), nullable=False))
    op.add_column('users', sa.Column('first_name', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False))
    op.add_column('users', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    
    # Rename 'hashed_password' to 'password_hash'
    op.alter_column('users', 'hashed_password', new_column_name='password_hash', existing_type=sa.String(length=100), nullable=False)
    
    # Create unique constraint for username
    op.create_unique_constraint('uq_users_username', 'users', ['username'])
    
    # Check if index for email already exists before creating it
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    indexes = inspector.get_indexes('users')
    index_names = [index['name'] for index in indexes]
    
    if 'ix_users_email' not in index_names:
        op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)


def downgrade() -> None:
     # Remove index on email if it exists
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    indexes = inspector.get_indexes('users')
    index_names = [index['name'] for index in indexes]
    
    if 'ix_users_email' in index_names:
        op.drop_index(op.f('ix_users_email'), table_name='users')
    
    # Remove unique constraint on username
    op.drop_constraint('uq_users_username', 'users', type_='unique')
    
    # Rename 'password_hash' back to 'hashed_password'
    op.alter_column('users', 'password_hash', new_column_name='hashed_password', existing_type=sa.String(length=100), nullable=False)
    
    # Drop new columns
    op.drop_column('users', 'deleted_at')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'username')
    
    # Rename 'user_id' back to 'id'
    op.alter_column('users', 'user_id', new_column_name='id', existing_type=sa.Integer(), autoincrement=True, nullable=False)
