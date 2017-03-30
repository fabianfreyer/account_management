"""

Make the priorities unique per uni, not globally.

Revision ID: 257e0b50e1b2
Revises: ba89e3b7438c
Create Date: 2017-04-01 19:02:39.512194

"""
from alembic import op
import sqlalchemy as sa
import IPython


# revision identifiers, used by Alembic.
revision = '257e0b50e1b2'
down_revision = 'ba89e3b7438c'
branch_labels = None
depends_on = None

naming_convention={
        "uq": "uq_%(table_name)s_%(column_0_name)s",
    }


def upgrade():
    with op.batch_alter_table('registration', naming_convention = naming_convention) as batch_op:
        batch_op.drop_constraint('uq_registration_priority', type_='unique')
        batch_op.create_unique_constraint('uq_registration_priority_uni', ['priority','uni_id'])


def downgrade():
    with op.batch_alter_table('registration', naming_convention = naming_convention) as batch_op:
        batch_op.drop_constraint('uq_registration_priority_uni', type_='unique')
        batch_op.create_unique_constraint('uq_registration_priority', ['priority'])
