"""Added bool check for times

Revision ID: 99998eb2198d
Revises: ee52a9d7d18f
Create Date: 2023-11-13 12:08:05.937573

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '99998eb2198d'
down_revision = 'ee52a9d7d18f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('announcements_new',
    sa.Column('masjid_id', sa.VARCHAR(length=16), nullable=False),
    sa.Column('date_issued', sa.Date(), nullable=False),
    sa.Column('date_expired', sa.Date(), nullable=True),
    sa.Column('message', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['masjid_id'], ['masjids.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('masjid_id', 'date_issued', 'message')
    )
    op.create_index(op.f('ix_announcements_new_masjid_id'), 'announcements_new', ['masjid_id'], unique=False)
    op.create_table('special_prayers_new',
    sa.Column('masjid_id', sa.VARCHAR(length=16), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('label', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('info', sa.String(), nullable=True),
    sa.Column('imam', sa.String(), nullable=True),
    sa.Column('start_time', sa.TIME(), nullable=True),
    sa.Column('jammat_time', sa.TIME(), nullable=False),
    sa.ForeignKeyConstraint(['masjid_id'], ['masjids.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('masjid_id', 'type', 'jammat_time', 'label')
    )
    op.create_index(op.f('ix_special_prayers_new_date'), 'special_prayers_new', ['date'], unique=False)
    op.create_index(op.f('ix_special_prayers_new_masjid_id'), 'special_prayers_new', ['masjid_id'], unique=False)
    op.drop_index('ix_special_prayers_date', table_name='special_prayers')
    op.drop_index('ix_special_prayers_masjid_id', table_name='special_prayers')
    op.drop_table('special_prayers')
    op.drop_index('ix_announcements_masjid_id', table_name='announcements')
    op.drop_table('announcements')
    op.add_column('masjids', sa.Column('has_times', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('masjids', 'has_times')
    op.create_table('announcements',
    sa.Column('masjid_id', sa.VARCHAR(length=16), autoincrement=False, nullable=False),
    sa.Column('date_issued', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('date_expired', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('message', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['masjid_id'], ['masjids.id'], name='announcements_masjid_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('masjid_id', 'date_expired', 'message', name='announcements_pkey')
    )
    op.create_index('ix_announcements_masjid_id', 'announcements', ['masjid_id'], unique=False)
    op.create_table('special_prayers',
    sa.Column('masjid_id', sa.VARCHAR(length=16), autoincrement=False, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('label', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('info', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('imam', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('start_time', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('jammat_time', postgresql.TIME(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['masjid_id'], ['masjids.id'], name='special_prayers_masjid_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('masjid_id', 'type', 'date', 'label', name='special_prayers_pkey')
    )
    op.create_index('ix_special_prayers_masjid_id', 'special_prayers', ['masjid_id'], unique=False)
    op.create_index('ix_special_prayers_date', 'special_prayers', ['date'], unique=False)
    op.drop_index(op.f('ix_special_prayers_new_masjid_id'), table_name='special_prayers_new')
    op.drop_index(op.f('ix_special_prayers_new_date'), table_name='special_prayers_new')
    op.drop_table('special_prayers_new')
    op.drop_index(op.f('ix_announcements_new_masjid_id'), table_name='announcements_new')
    op.drop_table('announcements_new')
    # ### end Alembic commands ###