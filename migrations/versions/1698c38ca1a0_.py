"""empty message

Revision ID: 1698c38ca1a0
Revises: 78f9cf39369f
Create Date: 2023-10-07 15:17:17.856686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1698c38ca1a0'
down_revision = '78f9cf39369f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Health', schema=None) as batch_op:
        batch_op.alter_column('age',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Health', schema=None) as batch_op:
        batch_op.alter_column('age',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
