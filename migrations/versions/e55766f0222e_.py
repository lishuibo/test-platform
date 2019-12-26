"""empty message

Revision ID: e55766f0222e
Revises: c2dc0dde0617
Create Date: 2019-12-11 16:50:02.577455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e55766f0222e'
down_revision = 'c2dc0dde0617'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('comment_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'comment', ['comment_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'comment_id')
    # ### end Alembic commands ###
