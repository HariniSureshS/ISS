"""empty message

Revision ID: 25d6b1be113a
Revises: f1dd95b862f3
Create Date: 2020-12-14 13:10:38.904087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25d6b1be113a'
down_revision = 'f1dd95b862f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cases', sa.Column('risk_factors', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('cases', sa.Column('similar_cases', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cases', 'similar_cases')
    op.drop_column('cases', 'risk_factors')
    # ### end Alembic commands ###