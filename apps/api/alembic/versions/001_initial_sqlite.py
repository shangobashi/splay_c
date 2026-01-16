"""Initial migration for SQLite (no Docker needed)

Revision ID: 001
Revises:
Create Date: 2026-01-14 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all tables for SQLite."""

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('subscription_tier', sa.String(20), nullable=False, server_default='free'),
        sa.Column('scans_this_month', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('email_verified', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_subscription_tier'), 'users', ['subscription_tier'], unique=False)

    # Create subscriptions table
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('plan', sa.String(20), nullable=False, server_default='free'),
        sa.Column('status', sa.String(20), nullable=False, server_default='active'),
        sa.Column('stripe_customer_id', sa.String(255), nullable=True),
        sa.Column('stripe_subscription_id', sa.String(255), nullable=True),
        sa.Column('current_period_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('current_period_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('cancel_at_period_end', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscriptions_user_id'), 'subscriptions', ['user_id'], unique=True)

    # Create products table
    op.create_table(
        'products',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('external_id', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('brand', sa.String(100), nullable=True),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False, server_default='USD'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('dimensions', sa.JSON(), nullable=True),
        sa.Column('colors', sa.JSON(), nullable=True),
        sa.Column('materials', sa.JSON(), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=False),
        sa.Column('images', sa.JSON(), nullable=True),
        sa.Column('affiliate_url', sa.Text(), nullable=False),
        sa.Column('retailer_url', sa.Text(), nullable=False),
        sa.Column('retailer_name', sa.String(100), nullable=False),
        sa.Column('embedding', sa.JSON(), nullable=True),  # Store as JSON instead of vector
        sa.Column('in_stock', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_external_id'), 'products', ['external_id'], unique=True)
    op.create_index(op.f('ix_products_brand'), 'products', ['brand'], unique=False)
    op.create_index(op.f('ix_products_category'), 'products', ['category'], unique=False)
    op.create_index(op.f('ix_products_retailer_name'), 'products', ['retailer_name'], unique=False)

    # Create scans table
    op.create_table(
        'scans',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('image_url', sa.Text(), nullable=False),
        sa.Column('thumbnail_url', sa.Text(), nullable=True),
        sa.Column('share_token', sa.String(64), nullable=True),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scans_user_id'), 'scans', ['user_id'], unique=False)
    op.create_index(op.f('ix_scans_status'), 'scans', ['status'], unique=False)
    op.create_index(op.f('ix_scans_created_at'), 'scans', ['created_at'], unique=False)
    op.create_index(op.f('ix_scans_share_token'), 'scans', ['share_token'], unique=True)

    # Create detected_items table
    op.create_table(
        'detected_items',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('scan_id', sa.String(36), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('bbox_x', sa.Float(), nullable=False),
        sa.Column('bbox_y', sa.Float(), nullable=False),
        sa.Column('bbox_width', sa.Float(), nullable=False),
        sa.Column('bbox_height', sa.Float(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('crop_url', sa.Text(), nullable=True),
        sa.Column('embedding', sa.JSON(), nullable=True),  # Store as JSON
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['scan_id'], ['scans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_detected_items_scan_id'), 'detected_items', ['scan_id'], unique=False)
    op.create_index(op.f('ix_detected_items_category'), 'detected_items', ['category'], unique=False)

    # Create item_matches table
    op.create_table(
        'item_matches',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('item_id', sa.String(36), nullable=False),
        sa.Column('product_id', sa.String(36), nullable=False),
        sa.Column('similarity_score', sa.Float(), nullable=False),
        sa.Column('is_budget_alternative', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], ['detected_items.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_matches_item_id'), 'item_matches', ['item_id'], unique=False)
    op.create_index(op.f('ix_item_matches_product_id'), 'item_matches', ['product_id'], unique=False)


def downgrade() -> None:
    """Drop all tables."""
    op.drop_index(op.f('ix_item_matches_product_id'), table_name='item_matches')
    op.drop_index(op.f('ix_item_matches_item_id'), table_name='item_matches')
    op.drop_table('item_matches')

    op.drop_index(op.f('ix_detected_items_category'), table_name='detected_items')
    op.drop_index(op.f('ix_detected_items_scan_id'), table_name='detected_items')
    op.drop_table('detected_items')

    op.drop_index(op.f('ix_scans_share_token'), table_name='scans')
    op.drop_index(op.f('ix_scans_created_at'), table_name='scans')
    op.drop_index(op.f('ix_scans_status'), table_name='scans')
    op.drop_index(op.f('ix_scans_user_id'), table_name='scans')
    op.drop_table('scans')

    op.drop_index(op.f('ix_products_retailer_name'), table_name='products')
    op.drop_index(op.f('ix_products_category'), table_name='products')
    op.drop_index(op.f('ix_products_brand'), table_name='products')
    op.drop_index(op.f('ix_products_external_id'), table_name='products')
    op.drop_table('products')

    op.drop_index(op.f('ix_subscriptions_user_id'), table_name='subscriptions')
    op.drop_table('subscriptions')

    op.drop_index(op.f('ix_users_subscription_tier'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
