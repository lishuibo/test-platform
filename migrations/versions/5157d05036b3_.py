"""empty message

Revision ID: 5157d05036b3
Revises: 764c173711e9
Create Date: 2019-12-04 14:29:33.101053

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5157d05036b3'
down_revision = '764c173711e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_user', sa.Column('_password', sa.String(length=100), nullable=False))
    op.drop_column('cms_user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_user', sa.Column('password', mysql.VARCHAR(length=100), nullable=False))
    op.drop_column('cms_user', '_password')
    # ### end Alembic commands ###
