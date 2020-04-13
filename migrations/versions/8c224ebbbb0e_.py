"""empty message

Revision ID: 8c224ebbbb0e
Revises: 78f4d0125f95
Create Date: 2020-04-13 20:02:06.376102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c224ebbbb0e'
down_revision = '78f4d0125f95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('word', sa.Column('part_of_speech', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('word', 'part_of_speech')
    # ### end Alembic commands ###
