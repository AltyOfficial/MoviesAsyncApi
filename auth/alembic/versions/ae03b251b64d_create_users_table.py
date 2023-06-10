"""Create users table.

Revision ID: ae03b251b64d
Revises: 
Create Date: 2023-06-08 18:56:27.863673

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'ae03b251b64d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()
    op.execute("CREATE SCHEMA IF NOT EXISTS auth")

    op.create_table(
        'auth.users',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(length=50)),
        sa.Column('created', sa.DateTime),
        sa.Column('modified', sa.DateTime),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_index('idx_users_id', 'auth.users', ['id'])
    connection.commit()


def downgrade() -> None:
    op.drop_table('auth.users')
