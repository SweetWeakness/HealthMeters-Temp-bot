"""empty message

Revision ID: 2a0ed7e04d04
Revises: 
Create Date: 2020-07-29 02:42:00.625264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a0ed7e04d04'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('guid', sa.String(length=36), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('telegram_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_user_telegram_id'), 'user', ['telegram_id'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_telegram_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
