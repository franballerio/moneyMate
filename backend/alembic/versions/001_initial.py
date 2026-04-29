"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2024-01-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'expenses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('item', sa.String(255), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('created_by', sa.String(10), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_expenses_id', 'expenses', ['id'])
    op.create_index('idx_expenses_category', 'expenses', ['category'])
    op.create_index('idx_expenses_date', 'expenses', ['date'])
    op.create_index('idx_expenses_category_date', 'expenses', ['category', 'date'])

    op.create_table(
        'budgets',
        sa.Column('id', sa.String(100), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('limit_amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('period', sa.String(20), nullable=False, server_default='monthly'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('category')
    )
    op.create_index('idx_budgets_category', 'budgets', ['category'])


def downgrade() -> None:
    op.drop_table('budgets')
    op.drop_table('expenses')