from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = 'ccb5c3d58063'
down_revision = None  # Update with the correct down_revision if needed
branch_labels = None
depends_on = None


def upgrade():
    # Create the custom ENUM type for 'setup_step'
    setupstep_enum = ENUM('email_verification', 'profile_completion', 'subscription_selection', 'completed', name='setupstep')
    setupstep_enum.create(op.get_bind(), checkfirst=True)

    # Create the 'comments', 'payments', 'posts', 'reel_comments', and 'reels' tables
    op.create_table('comments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('post_id', sa.UUID(), nullable=False),
        sa.Column('author_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id']),
        sa.ForeignKeyConstraint(['post_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)

    op.create_table('payments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('stripe_payment_id', sa.String(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('currency', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_id'), 'payments', ['id'], unique=False)

    op.create_table('posts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('author_id', sa.UUID(), nullable=False),
        sa.Column('likes', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)

    op.create_table('reel_comments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('reel_id', sa.UUID(), nullable=False),
        sa.Column('author_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id']),
        sa.ForeignKeyConstraint(['reel_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reel_comments_id'), 'reel_comments', ['id'], unique=False)

    op.create_table('reels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('author_id', sa.UUID(), nullable=False),
        sa.Column('likes', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reels_id'), 'reels', ['id'], unique=False)

    # Alter 'progress_photos' table to make sure 'user_id' column is UUID
    op.alter_column('progress_photos', 'user_id',
               existing_type=sa.UUID(),
               nullable=False)

    # Add the 'setup_step' column to 'users' table with the 'setupstep' ENUM type
    op.add_column('users', sa.Column('setup_step', setupstep_enum, nullable=True))


def downgrade():
    # Drop the 'setup_step' column
    op.drop_column('users', 'setup_step')

    # Alter the 'user_id' column in 'progress_photos' back to nullable
    op.alter_column('progress_photos', 'user_id',
               existing_type=sa.UUID(),
               nullable=True)

    # Drop the 'comments', 'payments', 'posts', 'reel_comments', and 'reels' tables
    op.drop_index(op.f('ix_reels_id'), table_name='reels')
    op.drop_table('reels')

    op.drop_index(op.f('ix_reel_comments_id'), table_name='reel_comments')
    op.drop_table('reel_comments')

    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_table('posts')

    op.drop_index(op.f('ix_payments_id'), table_name='payments')
    op.drop_table('payments')

    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')

    # Drop the 'setupstep' ENUM type
    setupstep_enum.drop(op.get_bind(), checkfirst=True)
