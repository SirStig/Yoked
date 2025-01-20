"""
Changed Enums

Revision ID: 8312b26f3aac
Revises: 2d1e100be8d4
Create Date: 2025-01-19 21:56:40.926274

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "8312b26f3aac"
down_revision = "2d1e100be8d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Update the `paymentstatus` enum to ensure correct values
    op.execute("ALTER TYPE paymentstatus ADD VALUE IF NOT EXISTS 'pending'")
    op.execute("ALTER TYPE paymentstatus ADD VALUE IF NOT EXISTS 'success'")
    op.execute("ALTER TYPE paymentstatus ADD VALUE IF NOT EXISTS 'failed'")


def downgrade() -> None:
    # Downgrade logic: drop the added values
    # Note: PostgreSQL does not support removing individual values from an enum directly
    # This typically involves creating a new enum type and swapping it in
    op.execute("CREATE TYPE paymentstatus_new AS ENUM ('success', 'failed')")
    op.execute("ALTER TABLE payments ALTER COLUMN status TYPE paymentstatus_new USING status::text::paymentstatus_new")
    op.execute("DROP TYPE paymentstatus")
    op.execute("ALTER TYPE paymentstatus_new RENAME TO paymentstatus")
