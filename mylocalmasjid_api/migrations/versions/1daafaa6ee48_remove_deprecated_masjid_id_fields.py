"""remove deprecated masjid_id fields

Revision ID: 1daafaa6ee48
Revises: a7451be87c86
Create Date: 2024-01-23 23:44:19.126888

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '1daafaa6ee48'
down_revision = 'a7451be87c86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('announcements', 'masjid_id')
    op.drop_column('facilities', 'masjid_id')
    op.drop_column('locations', 'masjid_id')
    op.drop_column('masjids', 'id')
    op.drop_column('prayer_times', 'masjid_id')
    op.drop_column('special_prayers', 'masjid_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('special_prayers', sa.Column('masjid_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('prayer_times', sa.Column('masjid_id', sa.VARCHAR(length=16), autoincrement=False, nullable=False))
    op.add_column('masjids', sa.Column('id', sa.VARCHAR(length=16), autoincrement=False, nullable=False))
    op.add_column('locations', sa.Column('masjid_id', sa.VARCHAR(length=16), autoincrement=False, nullable=False))
    op.add_column('facilities', sa.Column('masjid_id', sa.VARCHAR(length=16), autoincrement=False, nullable=False))
    op.add_column('announcements', sa.Column('masjid_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###