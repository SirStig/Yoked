"""Added Admin Models

Revision ID: cc34b1092a0c
Revises: 92dbc0803ad7
Create Date: 2025-01-21 23:36:14.150470

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc34b1092a0c'
down_revision: Union[str, None] = '92dbc0803ad7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create ENUM type for user_type
    usertype_enum = sa.Enum('REGULAR', 'ADMIN', name='usertype')
    usertype_enum.create(op.get_bind(), checkfirst=True)

    # Add user_type column with a default value for existing rows
    op.add_column('users', sa.Column('user_type', usertype_enum, nullable=False, server_default='REGULAR'))

    # Add admin_secret_key column with nullable=True
    op.add_column('users', sa.Column('admin_secret_key', sa.String(), nullable=True))

    # Add flagged_for_review column with nullable=False and a default value
    op.add_column('users', sa.Column('flagged_for_review', sa.Boolean(), nullable=False, server_default=sa.false()))

    # Remove server defaults to clean up
    op.alter_column('users', 'user_type', server_default=None)
    op.alter_column('users', 'flagged_for_review', server_default=None)


def downgrade() -> None:
    # Drop columns
    op.drop_column('users', 'flagged_for_review')
    op.drop_column('users', 'admin_secret_key')
    op.drop_column('users', 'user_type')

    # Drop ENUM type
    usertype_enum = sa.Enum('REGULAR', 'ADMIN', name='usertype')
    usertype_enum.drop(op.get_bind(), checkfirst=True)
