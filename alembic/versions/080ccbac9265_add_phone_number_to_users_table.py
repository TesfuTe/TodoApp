"""add phone number to users table

Revision ID: 080ccbac9265
Revises: 
Create Date: 2024-02-10 19:01:04.906365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '080ccbac9265'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column(
        'phone_number', sa.String(255), nullable=False))
    # the number 255 is only for myaql and maybe postgresql


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
