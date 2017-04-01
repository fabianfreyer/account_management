"""
Initial migration.

Revision ID: ba89e3b7438c
Revises:
Create Date: 2017-04-01 17:21:41.722009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba89e3b7438c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('uni',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=256), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('token')
    )
    op.create_table('registration',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=True),
    sa.Column('blob', sa.Text(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('uni_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uni_id'], ['uni.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('priority'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('registration')
    op.drop_table('uni')
    # ### end Alembic commands ###
