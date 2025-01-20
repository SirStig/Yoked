"""Payments added

Revision ID: c941f99cecc6
Revises: 606b5c2039f0
Create Date: 2025-01-19 10:42:55.544806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c941f99cecc6'
down_revision: Union[str, None] = '606b5c2039f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the custom ENUM types
    paymentplatform_enum = sa.Enum('STRIPE', 'GOOGLE', 'APPLE', name='paymentplatform')
    paymentstatus_enum = sa.Enum('SUCCESS', 'FAILED', 'PENDING', name='paymentstatus')
    paymentplatform_enum.create(op.get_bind())
    paymentstatus_enum.create(op.get_bind())

    # Add the new columns
    op.add_column('payments', sa.Column('google_payment_id', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('apple_payment_id', sa.String(), nullable=True))
    op.add_column('payments', sa.Column('platform', paymentplatform_enum, nullable=False))
    op.add_column('payments', sa.Column('status', paymentstatus_enum, nullable=False))
    op.add_column('payments', sa.Column('subscription_tier', sa.String(), nullable=False))
    op.add_column('payments', sa.Column('renewal_date', sa.DateTime(), nullable=True))
    op.alter_column('payments', 'stripe_payment_id',
               existing_type=sa.VARCHAR(),
               nullable=True)


def downgrade() -> None:
    # Drop the columns
    op.alter_column('payments', 'stripe_payment_id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('payments', 'renewal_date')
    op.drop_column('payments', 'subscription_tier')
    op.drop_column('payments', 'status')
    op.drop_column('payments', 'platform')
    op.drop_column('payments', 'apple_payment_id')
    op.drop_column('payments', 'google_payment_id')

    # Drop the ENUM types
    paymentplatform_enum = sa.Enum('STRIPE', 'GOOGLE', 'APPLE', name='paymentplatform')
    paymentstatus_enum = sa.Enum('SUCCESS', 'FAILED', 'PENDING', name='paymentstatus')
    paymentplatform_enum.drop(op.get_bind())
    paymentstatus_enum.drop(op.get_bind())
