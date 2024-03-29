"""added role to User Obj and added active fields to models

Revision ID: 8d52d9e443f7
Revises: c7c81cf8572f
Create Date: 2024-01-22 22:33:41.747631

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '8d52d9e443f7'
down_revision = 'c7c81cf8572f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('masjids', sa.Column('active', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('users', sa.Column('active', sa.Boolean(), nullable=True))
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('users', 'active')
    op.drop_column('users', 'role')
    op.drop_column('masjids', 'active')
    # ### end Alembic commands ###
