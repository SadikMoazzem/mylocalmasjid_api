"""re-added masjid_id fields

Revision ID: 80bfafef871f
Revises: a1598e5dfbf9
Create Date: 2024-01-24 00:03:14.928135

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '80bfafef871f'
down_revision = 'a1598e5dfbf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('announcements', sa.Column('masjid_id', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.create_foreign_key(None, 'announcements', 'masjids', ['masjid_id'], ['id'])
    op.add_column('facilities', sa.Column('masjid_id', sqlmodel.sql.sqltypes.GUID(), nullable=False))
    op.create_foreign_key(None, 'facilities', 'masjids', ['masjid_id'], ['id'])
    op.add_column('locations', sa.Column('masjid_id', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.create_foreign_key(None, 'locations', 'masjids', ['masjid_id'], ['id'])
    op.add_column('prayer_times', sa.Column('masjid_id', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.create_foreign_key(None, 'prayer_times', 'masjids', ['masjid_id'], ['id'])
    op.add_column('special_prayers', sa.Column('masjid_id', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.create_foreign_key(None, 'special_prayers', 'masjids', ['masjid_id'], ['id'])
    op.add_column('users', sa.Column('related_masjid', sqlmodel.sql.sqltypes.GUID(), nullable=True))
    op.create_foreign_key(None, 'users', 'masjids', ['related_masjid'], ['id'])
    op.drop_column('users', 'masjid_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('masjid_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'related_masjid')
    op.drop_constraint(None, 'special_prayers', type_='foreignkey')
    op.drop_column('special_prayers', 'masjid_id')
    op.drop_constraint(None, 'prayer_times', type_='foreignkey')
    op.drop_column('prayer_times', 'masjid_id')
    op.drop_constraint(None, 'locations', type_='foreignkey')
    op.drop_column('locations', 'masjid_id')
    op.drop_constraint(None, 'facilities', type_='foreignkey')
    op.drop_column('facilities', 'masjid_id')
    op.drop_constraint(None, 'announcements', type_='foreignkey')
    op.drop_column('announcements', 'masjid_id')
    # ### end Alembic commands ###
