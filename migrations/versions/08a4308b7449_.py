"""empty message

Revision ID: 08a4308b7449
Revises: 5b6693c2ef4c
Create Date: 2017-05-03 11:03:34.110928

"""

# revision identifiers, used by Alembic.
revision = '08a4308b7449'
down_revision = '5b6693c2ef4c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'node', ['name'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'node', type_='unique')
    ### end Alembic commands ###