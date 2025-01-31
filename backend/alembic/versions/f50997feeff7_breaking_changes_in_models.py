"""Breaking Changes in Models

Revision ID: f50997feeff7
Revises: d7f0f5523210
Create Date: 2025-01-30 22:28:18.699452

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f50997feeff7'
down_revision: Union[str, None] = 'd7f0f5523210'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('is_group_chat', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chats_id'), 'chats', ['id'], unique=False)
    op.create_table('meal_plans',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('diet_type', sa.String(), nullable=False),
    sa.Column('total_calories', sa.Integer(), nullable=False),
    sa.Column('protein_grams', sa.Integer(), nullable=True),
    sa.Column('carb_grams', sa.Integer(), nullable=True),
    sa.Column('fat_grams', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meal_plans_id'), 'meal_plans', ['id'], unique=False)
    op.create_table('tags',
    sa.Column('tag', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('tag')
    )
    op.create_table('workouts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('subcategory', sa.String(), nullable=True),
    sa.Column('muscle_groups', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('equipment', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('difficulty', sa.Enum('beginner', 'intermediate', 'advanced', name='difficultylevel'), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('video_vimeo_url', sa.String(), nullable=False),
    sa.Column('times_completed', sa.Integer(), nullable=True),
    sa.Column('likes_count', sa.Integer(), nullable=True),
    sa.Column('bookmarks_count', sa.Integer(), nullable=True),
    sa.Column('views_count', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_workouts_id'), 'workouts', ['id'], unique=False)
    op.create_table('friend_requests',
    sa.Column('sender_id', sa.UUID(), nullable=False),
    sa.Column('receiver_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('sender_id', 'receiver_id')
    )
    op.create_table('group_chat_participants',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('chat_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'chat_id')
    )
    op.create_table('messages',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('chat_id', sa.UUID(), nullable=False),
    sa.Column('sender_id', sa.UUID(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('image_s3_url', sa.String(), nullable=True),
    sa.Column('video_vimeo_url', sa.String(), nullable=True),
    sa.Column('is_edited', sa.Boolean(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('read_by', sa.ARRAY(sa.UUID()), nullable=True),
    sa.Column('reactions', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)
    op.create_table('nutrition_articles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('author_id', sa.UUID(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('tags', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nutrition_articles_id'), 'nutrition_articles', ['id'], unique=False)
    op.create_table('posts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('author_id', sa.UUID(), nullable=False),
    sa.Column('image_s3_url', sa.String(), nullable=True),
    sa.Column('video_vimeo_url', sa.String(), nullable=True),
    sa.Column('likes_count', sa.Integer(), nullable=True),
    sa.Column('shares_count', sa.Integer(), nullable=True),
    sa.Column('comments_count', sa.Integer(), nullable=True),
    sa.Column('views_count', sa.Integer(), nullable=True),
    sa.Column('is_pinned', sa.Boolean(), nullable=True),
    sa.Column('is_reported', sa.Boolean(), nullable=True),
    sa.Column('visibility', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.create_table('progress_photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('uploaded_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_progress_photos_id'), 'progress_photos', ['id'], unique=False)
    op.create_table('reels',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('author_id', sa.UUID(), nullable=False),
    sa.Column('video_vimeo_url', sa.String(), nullable=False),
    sa.Column('thumbnail_s3_url', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('likes_count', sa.Integer(), nullable=True),
    sa.Column('shares_count', sa.Integer(), nullable=True),
    sa.Column('comments_count', sa.Integer(), nullable=True),
    sa.Column('views_count', sa.Integer(), nullable=True),
    sa.Column('is_advertisement', sa.Boolean(), nullable=True),
    sa.Column('advertiser_id', sa.UUID(), nullable=True),
    sa.Column('is_reported', sa.Boolean(), nullable=True),
    sa.Column('visibility', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['advertiser_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reels_id'), 'reels', ['id'], unique=False)
    op.create_table('saved_meal_plans',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('meal_plan_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['meal_plan_id'], ['meal_plans.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'meal_plan_id')
    )
    op.create_table('typing_status',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('chat_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('is_typing', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_typing_status_id'), 'typing_status', ['id'], unique=False)
    op.create_table('user_followers',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('follower_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'follower_id')
    )
    op.create_table('user_meal_tracking',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('meal_plan_id', sa.UUID(), nullable=True),
    sa.Column('date_tracked', sa.DateTime(), nullable=False),
    sa.Column('calories_consumed', sa.Integer(), nullable=False),
    sa.Column('protein_grams', sa.Integer(), nullable=True),
    sa.Column('carb_grams', sa.Integer(), nullable=True),
    sa.Column('fat_grams', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['meal_plan_id'], ['meal_plans.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_meal_tracking_id'), 'user_meal_tracking', ['id'], unique=False)
    op.create_table('user_subscriptions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('subscription_tier_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('renewal_date', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['subscription_tier_id'], ['subscription_tiers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_subscriptions_user_id'), 'user_subscriptions', ['user_id'], unique=False)
    op.create_table('workout_bookmarks',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('workout_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'workout_id')
    )
    op.create_table('workout_progress',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('workout_id', sa.UUID(), nullable=False),
    sa.Column('completed_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workout_progress_id'), 'workout_progress', ['id'], unique=False)
    op.create_table('workout_tags',
    sa.Column('workout_id', sa.UUID(), nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['tag'], ['tags.tag'], ),
    sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], ),
    sa.PrimaryKeyConstraint('workout_id', 'tag')
    )
    op.create_table('comments',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('post_id', sa.UUID(), nullable=False),
    sa.Column('author_id', sa.UUID(), nullable=False),
    sa.Column('likes_count', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_table('post_bookmarks',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('post_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.create_table('post_likes',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('post_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.create_table('post_tags',
    sa.Column('post_id', sa.UUID(), nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['tag'], ['tags.tag'], ),
    sa.PrimaryKeyConstraint('post_id', 'tag')
    )
    op.create_table('reel_bookmarks',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('reel_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['reel_id'], ['reels.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'reel_id')
    )
    op.create_table('reel_comments',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('reel_id', sa.UUID(), nullable=False),
    sa.Column('author_id', sa.UUID(), nullable=False),
    sa.Column('likes_count', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['reel_id'], ['reels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reel_comments_id'), 'reel_comments', ['id'], unique=False)
    op.create_table('reel_likes',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('reel_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['reel_id'], ['reels.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'reel_id')
    )
    op.create_table('reel_tags',
    sa.Column('reel_id', sa.UUID(), nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['reel_id'], ['reels.id'], ),
    sa.ForeignKeyConstraint(['tag'], ['tags.tag'], ),
    sa.PrimaryKeyConstraint('reel_id', 'tag')
    )
    op.create_table('reported_posts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('post_id', sa.UUID(), nullable=False),
    sa.Column('reporter_id', sa.UUID(), nullable=False),
    sa.Column('reason', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['reporter_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reported_posts_id'), 'reported_posts', ['id'], unique=False)
    op.create_table('reported_reels',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('reel_id', sa.UUID(), nullable=False),
    sa.Column('reporter_id', sa.UUID(), nullable=False),
    sa.Column('reason', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['reel_id'], ['reels.id'], ),
    sa.ForeignKeyConstraint(['reporter_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reported_reels_id'), 'reported_reels', ['id'], unique=False)
    op.drop_table('user_friends')
    op.add_column('payments', sa.Column('subscription_id', sa.UUID(), nullable=True))
    op.drop_constraint('payments_subscription_tier_id_fkey', 'payments', type_='foreignkey')
    op.create_foreign_key(None, 'payments', 'user_subscriptions', ['subscription_id'], ['id'])
    op.drop_column('payments', 'subscription_tier_id')
    op.add_column('sessions', sa.Column('device_os', sa.String(), nullable=True))
    op.add_column('sessions', sa.Column('browser', sa.String(), nullable=True))
    op.alter_column('sessions', 'user_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.create_index(op.f('ix_sessions_user_id'), 'sessions', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sessions_user_id'), table_name='sessions')
    op.alter_column('sessions', 'user_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.drop_column('sessions', 'browser')
    op.drop_column('sessions', 'device_os')
    op.add_column('payments', sa.Column('subscription_tier_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'payments', type_='foreignkey')
    op.create_foreign_key('payments_subscription_tier_id_fkey', 'payments', 'subscription_tiers', ['subscription_tier_id'], ['id'])
    op.drop_column('payments', 'subscription_id')
    op.create_table('user_friends',
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('friend_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['friend_id'], ['users.id'], name='user_friends_friend_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_friends_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'friend_id', name='user_friends_pkey')
    )
    op.drop_index(op.f('ix_reported_reels_id'), table_name='reported_reels')
    op.drop_table('reported_reels')
    op.drop_index(op.f('ix_reported_posts_id'), table_name='reported_posts')
    op.drop_table('reported_posts')
    op.drop_table('reel_tags')
    op.drop_table('reel_likes')
    op.drop_index(op.f('ix_reel_comments_id'), table_name='reel_comments')
    op.drop_table('reel_comments')
    op.drop_table('reel_bookmarks')
    op.drop_table('post_tags')
    op.drop_table('post_likes')
    op.drop_table('post_bookmarks')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    op.drop_table('workout_tags')
    op.drop_index(op.f('ix_workout_progress_id'), table_name='workout_progress')
    op.drop_table('workout_progress')
    op.drop_table('workout_bookmarks')
    op.drop_index(op.f('ix_user_subscriptions_user_id'), table_name='user_subscriptions')
    op.drop_table('user_subscriptions')
    op.drop_index(op.f('ix_user_meal_tracking_id'), table_name='user_meal_tracking')
    op.drop_table('user_meal_tracking')
    op.drop_table('user_followers')
    op.drop_index(op.f('ix_typing_status_id'), table_name='typing_status')
    op.drop_table('typing_status')
    op.drop_table('saved_meal_plans')
    op.drop_index(op.f('ix_reels_id'), table_name='reels')
    op.drop_table('reels')
    op.drop_index(op.f('ix_progress_photos_id'), table_name='progress_photos')
    op.drop_table('progress_photos')
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_table('posts')
    op.drop_index(op.f('ix_nutrition_articles_id'), table_name='nutrition_articles')
    op.drop_table('nutrition_articles')
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')
    op.drop_table('group_chat_participants')
    op.drop_table('friend_requests')
    op.drop_index(op.f('ix_workouts_id'), table_name='workouts')
    op.drop_table('workouts')
    op.drop_table('tags')
    op.drop_index(op.f('ix_meal_plans_id'), table_name='meal_plans')
    op.drop_table('meal_plans')
    op.drop_index(op.f('ix_chats_id'), table_name='chats')
    op.drop_table('chats')
    # ### end Alembic commands ###
