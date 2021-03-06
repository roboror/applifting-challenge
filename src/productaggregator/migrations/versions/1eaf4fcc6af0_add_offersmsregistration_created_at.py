"""add offersmsregistration.created_at

Revision ID: 1eaf4fcc6af0
Revises: 5fd6a2e01bb2
Create Date: 2020-08-28 20:33:56.136796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1eaf4fcc6af0'
down_revision = '5fd6a2e01bb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offers_ms_registration', sa.Column('created_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('offers_ms_registration', 'created_date')
    # ### end Alembic commands ###
