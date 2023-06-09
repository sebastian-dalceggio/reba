"""empty message

Revision ID: a277d9d55446
Revises: 
Create Date: 2023-06-09 11:34:45.906611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a277d9d55446'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('indice_aperturas',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, cycle=True), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('region', sa.String(length=50), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'region', 'category', name='one_value_per_datetime_per_region_per_category')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('indice_aperturas')
    # ### end Alembic commands ###