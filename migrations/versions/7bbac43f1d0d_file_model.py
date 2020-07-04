"""File model

Revision ID: 7bbac43f1d0d
Revises: 7117c9ee95cf
Create Date: 2020-07-03 15:25:13.958062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bbac43f1d0d'
down_revision = '7117c9ee95cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=120), nullable=True),
    sa.Column('extension', sa.String(length=10), nullable=True),
    sa.Column('size', sa.String(length=120), nullable=True),
    sa.Column('path', sa.String(length=120), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file')
    # ### end Alembic commands ###