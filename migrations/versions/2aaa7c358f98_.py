"""empty message

Revision ID: 2aaa7c358f98
Revises: d24f3b3b22b5
Create Date: 2019-08-13 13:23:27.728138

"""

# revision identifiers, used by Alembic.
revision = '2aaa7c358f98'
down_revision = 'd24f3b3b22b5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participantes', sa.Column('nombre', sa.String(), nullable=True))
    op.drop_column('participantes', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participantes', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('participantes', 'nombre')
    # ### end Alembic commands ###
