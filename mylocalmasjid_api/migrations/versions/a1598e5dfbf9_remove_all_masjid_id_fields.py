"""remove all masjid_id fields

Revision ID: a1598e5dfbf9
Revises: 1daafaa6ee48
Create Date: 2024-01-23 23:52:31.815567

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'a1598e5dfbf9'
down_revision = '1daafaa6ee48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_announcements_new_masjid_id_masjids', 'announcements', type_='foreignkey')
    op.drop_column('announcements', 'new_masjid_id')
    op.drop_constraint('fk_facilities_new_masjid_id_masjids', 'facilities', type_='foreignkey')
    op.drop_column('facilities', 'new_masjid_id')
    op.drop_constraint('fk_locations_new_masjid_id_masjids', 'locations', type_='foreignkey')
    op.drop_column('locations', 'new_masjid_id')
    # op.add_column('masjids', sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False))
    # op.drop_column('masjids', 'new_id')
    op.drop_constraint('fk_prayer_times_new_masjid_id_masjids', 'prayer_times', type_='foreignkey')
    op.drop_column('prayer_times', 'new_masjid_id')
    op.drop_constraint('fk_special_prayers_new_masjid_id_masjids', 'special_prayers', type_='foreignkey')
    op.drop_column('special_prayers', 'new_masjid_id')
    # ### end Alembic commands ###

    op.drop_constraint('masjids_pkey', 'masjids', type_='primary')
    op.alter_column('masjids', 'new_id', nullable=False, new_column_name='id')
    op.create_primary_key('masjids_pkey', 'masjids', ['id'])


def downgrade():
    op.drop_constraint('masjids_pkey', 'masjids', type_='primary')
    op.alter_column('masjids', 'id', nullable=False, new_column_name='new_id')
    op.create_primary_key('masjids_pkey', 'masjids', ['new_id'])

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('special_prayers', sa.Column('new_masjid_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('fk_special_prayers_new_masjid_id_masjids', 'special_prayers', 'masjids', ['new_masjid_id'], ['new_id'])
    op.add_column('prayer_times', sa.Column('new_masjid_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('fk_prayer_times_new_masjid_id_masjids', 'prayer_times', 'masjids', ['new_masjid_id'], ['new_id'])
    # op.add_column('masjids', sa.Column('new_id', sa.UUID(), autoincrement=False, nullable=False))
    # op.drop_column('masjids', 'id')
    op.add_column('locations', sa.Column('new_masjid_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('fk_locations_new_masjid_id_masjids', 'locations', 'masjids', ['new_masjid_id'], ['new_id'])
    op.add_column('facilities', sa.Column('new_masjid_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('fk_facilities_new_masjid_id_masjids', 'facilities', 'masjids', ['new_masjid_id'], ['new_id'])
    op.add_column('announcements', sa.Column('new_masjid_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('fk_announcements_new_masjid_id_masjids', 'announcements', 'masjids', ['new_masjid_id'], ['new_id'])
    # ### end Alembic commands ###
