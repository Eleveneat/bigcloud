"""init

Revision ID: dc1599a03e7c
Revises: 6c128af86770
Create Date: 2017-02-23 14:34:29.357159

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'dc1599a03e7c'
down_revision = '6c128af86770'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appgroups', sa.Column('修改时间', sa.DateTime(), nullable=True))
    op.add_column('appgroups', sa.Column('创建时间', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('appgroups', '创建时间')
    op.drop_column('appgroups', '修改时间')
    # ### end Alembic commands ###
