"""Init migration

Revision ID: f2c97c0e97c0
Revises: 
Create Date: 2025-10-31 20:49:03.070807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2c97c0e97c0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('monthly_income', sa.Integer(), nullable=False),
    sa.Column('employment_type', sa.Enum('FULL_TIME', 'FREELANCE', 'UNEMPLOYED', name='employmenttype'), nullable=False),
    sa.Column('has_property', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('creditnote',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('loan_id', sa.String(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('issue_date', sa.Date(), nullable=False),
    sa.Column('term_days', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('OPEN', 'CLOSED', name='creditstatus'), nullable=False),
    sa.Column('close_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('creditnote')
    op.drop_table('user')
    # ### end Alembic commands ###
