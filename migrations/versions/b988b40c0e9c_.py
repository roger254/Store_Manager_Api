"""empty message

Revision ID: b988b40c0e9c
Revises:
Create Date: 2018-10-17 22:12:46.721849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b988b40c0e9c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('product_name', sa.String(
                        length=255), nullable=True),
                    sa.Column('product_price', sa.Float(), nullable=True),
                    sa.Column('product_quantity', sa.Integer(), nullable=True),
                    sa.Column('product_entry_date',
                              sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###
