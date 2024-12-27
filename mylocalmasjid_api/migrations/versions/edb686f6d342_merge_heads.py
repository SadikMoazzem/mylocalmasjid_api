"""merge heads

Revision ID: edb686f6d342
Revises: e4e5717208a4, e4e571720a4
Create Date: 2024-12-26 00:57:39.186679

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'edb686f6d342'
down_revision = ('e4e5717208a4', 'e4e571720a4')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
