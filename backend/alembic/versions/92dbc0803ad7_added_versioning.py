"""Added Versioning

Revision ID: 92dbc0803ad7
Revises: 171cd302be18
Create Date: 2025-01-20 22:23:04.849152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92dbc0803ad7'
down_revision: Union[str, None] = '171cd302be18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'version' column to 'subscription_tiers' table with a default value of 1
    op.add_column('subscription_tiers', sa.Column('version', sa.Integer(), nullable=False, server_default='1'))
    # Remove the default after populating existing rows
    op.alter_column('subscription_tiers', 'version', server_default=None)

    # Add 'profile_version' column to 'users' table with a default value of 1
    op.add_column('users', sa.Column('profile_version', sa.Integer(), nullable=False, server_default='1'))
    # Remove the default after populating existing rows
    op.alter_column('users', 'profile_version', server_default=None)


def downgrade() -> None:
    # Drop the columns in case of downgrade
    op.drop_column('users', 'profile_version')
    op.drop_column('subscription_tiers', 'version')
