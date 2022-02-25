"""empty message

Revision ID: b0b650200872
Revises: ba4a2857733f
Create Date: 2022-02-26 03:04:58.665965

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b0b650200872'
down_revision = 'ba4a2857733f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=mysql.VARCHAR(length=16),
               type_=sa.String(length=64),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password',
               existing_type=sa.String(length=64),
               type_=mysql.VARCHAR(length=16),
               existing_nullable=False)
    # ### end Alembic commands ###
