"""user_wallets_one_to_one

Revision ID: 437de1a1e771
Revises: 6936a3adeaab
Create Date: 2021-05-18 18:24:57.517171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '437de1a1e771'
down_revision = '6936a3adeaab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq_wallets_owner_id'), 'wallets', ['owner_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_wallets_owner_id'), 'wallets', type_='unique')
    # ### end Alembic commands ###
