"""empty message

Revision ID: 66285a4c40de
Revises: None
Create Date: 2016-10-26 15:16:06.819011

"""

# revision identifiers, used by Alembic.
revision = '66285a4c40de'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.String(length=11), nullable=False),
    sa.Column('receiver', sa.String(length=11), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=True),
    sa.Column('status_code', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    ### end Alembic commands ###
