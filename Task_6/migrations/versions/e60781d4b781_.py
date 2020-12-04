"""empty message

Revision ID: e60781d4b781
Revises: f967e3f06171
Create Date: 2020-12-03 14:57:53.464884

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e60781d4b781'
down_revision = 'f967e3f06171'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cases', sa.Column('embedding', sa.ARRAY(sa.Float()), nullable=True))
    op.add_column('cases', sa.Column('keywords', sa.ARRAY(sa.Text()), nullable=True))
    op.add_column('cases', sa.Column('risk_score', sa.Float(), nullable=True))
    op.add_column('cases', sa.Column('summary', sa.Text(), nullable=True))
    op.add_column('cases', sa.Column('topic_word', sa.String(), nullable=True))
    op.drop_column('cases', 'embeddings')
    op.drop_column('cases', 'embeddings_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cases', sa.Column('embeddings_date', sa.DATE(), autoincrement=False, nullable=True))
    op.add_column('cases', sa.Column('embeddings', postgresql.ARRAY(postgresql.DOUBLE_PRECISION(precision=53)), autoincrement=False, nullable=True))
    op.drop_column('cases', 'topic_word')
    op.drop_column('cases', 'summary')
    op.drop_column('cases', 'risk_score')
    op.drop_column('cases', 'keywords')
    op.drop_column('cases', 'embedding')
    # ### end Alembic commands ###
