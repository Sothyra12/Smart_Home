# Alembic Migration Guide

## Prerequisites

Make sure Alembic is installed in your environment. If not, you can install it using pip:

```sh
pip install alembic
```

## Initial Setup
1. Initialize Alembic in your project:

```
alembic init alembic
```

This will create an alembic directory and an alembic.ini configuration file.

1. Configure Alembic:

Edit the alembic.ini file and set the SQLAlchemy URL to your database:

```
sqlalchemy.url = postgresql://user:password@localhost/dbname
```

Edit alembic/env.py to include your models. Modify the target_metadata line:

```
from myapp.db.base import Base  # Import your Base from your app
target_metadata = Base.metadata
```


### Creating a New Migration
1. Generate a New Migration Script:
```
alembic revision -m "description of the migration"
```
This will create a new migration script in the alembic/versions directory with a unique identifier.
1. Edit the Migration Script:

Open the generated migration script and define the changes in the upgrade and downgrade functions.

Example:

"""create chats and chat_messages tables with foreign keys

Revision ID: 1234567890ab
Revises: abcdef123456
Create Date: 2024-07-20 19:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

## Revision identifiers, used by Alembic.
revision = '1234567890ab'
down_revision = 'abcdef123456'
branch_labels = None
depends_on = None

def upgrade():
    # Create the chats table
    op.create_table(
        'chats',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now(), nullable=False)
    )

    # Create the chat_messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('chat_id', sa.Integer, sa.ForeignKey('chats.id'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True),
        sa.Column('sender_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('timestamp', sa.DateTime, default=sa.func.utcnow)
    )

def downgrade():
    # Drop the chat_messages table if we need to downgrade
    op.drop_table('chat_messages')

    # Drop the chats table if we need to downgrade
    op.drop_table('chats')


## Applying Migrations
1. Apply the Migration to your database:
```
alembic upgrade head
```

This will apply all unapplied migrations up to the latest one.

### Additional Commands
Revising a Migration: To create a new migration based on changes detected automatically, you can use:
```
alembic revision --autogenerate -m "description of the migration"
```

#### Downgrading a Migration: To revert the database to a previous migration, use:
```
alembic downgrade -1
```
This will revert the database one revision back. You can specify a specific revision instead of -1.

#### Viewing Migration History: To see the list of migrations applied, use:
```
alembic history
```
#### Checking Current Revision: To see the current revision applied to the database, use:

```
alembic current
```
