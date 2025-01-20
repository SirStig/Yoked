"""Add subscription_tier_id to payments

Revision ID: 0c95d0145eac
Revises: 0a76943f1fda
Create Date: 2025-01-19 21:51:44.009766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c95d0145eac'
down_revision: Union[str, None] = '0a76943f1fda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('subscription_tier_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'payments', 'subscription_tiers', ['subscription_tier_id'], ['id'])
    op.drop_column('payments', 'subscription_tier')
    op.alter_column('subscription_tiers', 'recurring_interval',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subscription_tiers', 'recurring_interval',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.add_column('payments', sa.Column('subscription_tier', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'payments', type_='foreignkey')
    op.drop_column('payments', 'subscription_tier_id')
    # ### end Alembic commands ###
