"""add_logs_table

Revision ID: e4e571720a4
Revises: 0cba8268bf04
Create Date: 2024-01-25 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'e4e571720a4'
down_revision = '0cba8268bf04'
branch_labels = None
depends_on = None


def upgrade():
    # Create logs table
    op.create_table('logs',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('masjid_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('action_time', sa.DateTime(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),  # Using String instead of Enum
        sa.Column('entity_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('entity_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('details', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(['masjid_id'], ['masjids.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('logs') 