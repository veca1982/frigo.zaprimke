"""empty message

Revision ID: e9100ff3b3d9
Revises: 
Create Date: 2017-08-09 16:35:54.014000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e9100ff3b3d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cijena_1',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cijena_kn_kg', sa.Float(), nullable=True),
    sa.Column('datum_od', sa.Date(), nullable=True),
    sa.Column('datum_do', sa.Date(), nullable=True),
    sa.Column('tstapm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='frigo'
    )
    op.create_table('cijena_1x',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cijena_kn_kg', sa.Float(), nullable=True),
    sa.Column('datum_od', sa.Date(), nullable=True),
    sa.Column('datum_do', sa.Date(), nullable=True),
    sa.Column('tstapm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='frigo'
    )
    op.create_table('cijena_2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cijena_kn_kg', sa.Float(), nullable=True),
    sa.Column('datum_od', sa.Date(), nullable=True),
    sa.Column('datum_do', sa.Date(), nullable=True),
    sa.Column('tstapm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='frigo'
    )
    op.create_table('cijena_3',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cijena_kn_kg', sa.Float(), nullable=True),
    sa.Column('datum_od', sa.Date(), nullable=True),
    sa.Column('datum_do', sa.Date(), nullable=True),
    sa.Column('tstapm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='frigo'
    )
    op.create_table('cijena_4',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cijena_kn_kg', sa.Float(), nullable=True),
    sa.Column('datum_od', sa.Date(), nullable=True),
    sa.Column('datum_do', sa.Date(), nullable=True),
    sa.Column('tstapm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='frigo'
    )
    op.create_table('cijena_5',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cijena_kn_kg', sa.Float(), nullable=True),
    sa.Column('datum_od', sa.Date(), nullable=True),
    sa.Column('datum_do', sa.Date(), nullable=True),
    sa.Column('tstapm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='frigo'
    )
    op.create_table('departments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='frigo'
    )
    op.create_table('koperanti',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ime', sa.String(), nullable=False),
    sa.Column('prezime', sa.String(), nullable=False),
    sa.Column('global_gap', sa.Boolean(), nullable=False),
    sa.Column('tstapm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='frigo'
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='frigo'
    )
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['frigo.departments.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['frigo.roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='frigo'
    )
    op.create_index(op.f('ix_frigo_employees_email'), 'employees', ['email'], unique=True, schema='frigo')
    op.create_index(op.f('ix_frigo_employees_first_name'), 'employees', ['first_name'], unique=False, schema='frigo')
    op.create_index(op.f('ix_frigo_employees_last_name'), 'employees', ['last_name'], unique=False, schema='frigo')
    op.create_index(op.f('ix_frigo_employees_username'), 'employees', ['username'], unique=True, schema='frigo')
    op.create_table('zaprimka',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_koperanta', sa.Integer(), nullable=False),
    sa.Column('brutto_masa', sa.Float(), nullable=False),
    sa.Column('vl_gajbi', sa.Integer(), nullable=False),
    sa.Column('kop_gajbi', sa.Integer(), nullable=False),
    sa.Column('regija', sa.String(), nullable=False),
    sa.Column('masa_kalib_1x', sa.Float(), nullable=True),
    sa.Column('masa_kalib_1', sa.Float(), nullable=True),
    sa.Column('masa_kalib_2', sa.Float(), nullable=True),
    sa.Column('masa_kalib_3', sa.Float(), nullable=True),
    sa.Column('masa_kalib_4', sa.Float(), nullable=True),
    sa.Column('masa_kalib_5', sa.Float(), nullable=True),
    sa.Column('otpad_masa', sa.Float(), nullable=True),
    sa.Column('netto_masa', sa.Float(), nullable=True),
    sa.Column('barcode', postgresql.BYTEA(), nullable=True),
    sa.Column('cijena_kn', sa.Float(), nullable=True),
    sa.Column('cijena_1x', sa.Integer(), nullable=True),
    sa.Column('cijena_1', sa.Integer(), nullable=True),
    sa.Column('cijena_2', sa.Integer(), nullable=True),
    sa.Column('cijena_3', sa.Integer(), nullable=True),
    sa.Column('cijena_4', sa.Integer(), nullable=True),
    sa.Column('cijena_5', sa.Integer(), nullable=True),
    sa.Column('datum_zaprimanja', sa.Date(), nullable=True),
    sa.Column('datum_kalibracije', sa.Date(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('tstamp', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.ForeignKeyConstraint(['cijena_1'], ['frigo.cijena_1.id'], ),
    sa.ForeignKeyConstraint(['cijena_1x'], ['frigo.cijena_1x.id'], ),
    sa.ForeignKeyConstraint(['cijena_2'], ['frigo.cijena_2.id'], ),
    sa.ForeignKeyConstraint(['cijena_3'], ['frigo.cijena_3.id'], ),
    sa.ForeignKeyConstraint(['cijena_4'], ['frigo.cijena_4.id'], ),
    sa.ForeignKeyConstraint(['cijena_5'], ['frigo.cijena_5.id'], ),
    sa.ForeignKeyConstraint(['id_koperanta'], ['frigo.koperanti.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='frigo'
    )
    #op.drop_table('meta_data_about_image_getting')
    #op.drop_table('korisnici')
    #op.drop_table('korisnik_data')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('korisnik_data',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id_korisnika', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('slika', postgresql.BYTEA(), autoincrement=False, nullable=False),
    sa.Column('predicted', sa.VARCHAR(length=7), autoincrement=False, nullable=False),
    sa.Column('stanje', sa.REAL(), autoincrement=False, nullable=False),
    sa.Column('tstamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_korisnika'], [u'korisnici.id'], name=u'korisnik_data_id_korisnika_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'korisnik_data_pkey')
    )
    op.create_table('korisnici',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('oib', sa.VARCHAR(length=12), autoincrement=False, nullable=True),
    sa.Column('device_ip_adress', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('salary', sa.REAL(), autoincrement=False, nullable=True),
    sa.Column('tstamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('path_to_image', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'korisnici_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('meta_data_about_image_getting',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id_korisnika', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', sa.CHAR(length=1), autoincrement=False, nullable=False),
    sa.Column('time_last_pic_taken', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_korisnika'], [u'korisnici.id'], name=u'last_pic_taken_for_korisnik_id_korisnika_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'last_pic_taken_for_korisnik_pkey')
    )
    op.drop_table('zaprimka', schema='frigo_new')
    op.drop_index(op.f('ix_frigo_new_employees_username'), table_name='employees', schema='frigo_new')
    op.drop_index(op.f('ix_frigo_new_employees_last_name'), table_name='employees', schema='frigo_new')
    op.drop_index(op.f('ix_frigo_new_employees_first_name'), table_name='employees', schema='frigo_new')
    op.drop_index(op.f('ix_frigo_new_employees_email'), table_name='employees', schema='frigo_new')
    op.drop_table('employees', schema='frigo_new')
    op.drop_table('roles', schema='frigo_new')
    op.drop_table('koperanti', schema='frigo_new')
    op.drop_table('departments', schema='frigo_new')
    op.drop_table('cijena_5', schema='frigo_new')
    op.drop_table('cijena_4', schema='frigo_new')
    op.drop_table('cijena_3', schema='frigo_new')
    op.drop_table('cijena_2', schema='frigo_new')
    op.drop_table('cijena_1x', schema='frigo_new')
    op.drop_table('cijena_1', schema='frigo_new')
    # ### end Alembic commands ###
