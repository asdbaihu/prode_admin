"""empty message

Revision ID: fab7fba9fd92
Revises: 8c26e52bcb49
Create Date: 2019-08-12 17:14:37.029208

"""

# revision identifiers, used by Alembic.
revision = 'fab7fba9fd92'
down_revision = '8c26e52bcb49'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('partidos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha_id', sa.Integer(), nullable=False),
    sa.Column('local', sa.String(), nullable=True),
    sa.Column('visitante', sa.String(), nullable=True),
    sa.Column('resultado', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['fecha_id'], ['partidos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fechas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prode_id', sa.Integer(), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prode_id'], ['prodes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pronosticos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('participante_id', sa.Integer(), nullable=False),
    sa.Column('partido_id', sa.Integer(), nullable=False),
    sa.Column('resultado', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['participante_id'], ['participantes.id'], ),
    sa.ForeignKeyConstraint(['partido_id'], ['partidos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Pronosticos')
    op.drop_table('Fechas')
    op.drop_table('Partidos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Partidos',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Partidos_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('fecha_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('local', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('visitante', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('resultado', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['fecha_id'], ['Partidos.id'], name='Partidos_fecha_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Partidos_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('Fechas',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Fechas_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('prode_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('cantidad', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['prode_id'], ['prodes.id'], name='Fechas_prode_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Fechas_pkey')
    )
    op.create_table('Pronosticos',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Pronosticos_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('participante_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('partido_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('resultado', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['participante_id'], ['participantes.id'], name='Pronosticos_participante_id_fkey'),
    sa.ForeignKeyConstraint(['partido_id'], ['Partidos.id'], name='Pronosticos_partido_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Pronosticos_pkey')
    )
    op.drop_table('pronosticos')
    op.drop_table('fechas')
    op.drop_table('partidos')
    # ### end Alembic commands ###