"""Add products

Revision ID: bfe1031465ad
Revises: f2c97c0e97c0
Create Date: 2025-11-05 17:08:39.335835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bfe1031465ad'
down_revision: Union[str, Sequence[str], None] = 'f2c97c0e97c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('max_amount', sa.Integer(), nullable=False),
    sa.Column('term_days', sa.Integer(), nullable=False),
    sa.Column('interest_rate_daily', sa.Float(), nullable=False),
    sa.Column('client_type', sa.Enum('PIONEER', 'REPEATER', name='clienttype'), nullable=False),
    sa.CheckConstraint('interest_rate_daily > 0', name='check_interest_rate_positive'),
    sa.CheckConstraint('max_amount > 0', name='check_max_amount_positive'),
    sa.CheckConstraint('term_days > 0', name='check_term_days_positive'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('products')
    # ### end Alembic commands ###
