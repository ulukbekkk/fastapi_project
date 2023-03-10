"""secondd

Revision ID: e0e672eec184
Revises: b7e105eeb145
Create Date: 2022-12-17 12:29:01.968458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0e672eec184'
down_revision = 'b7e105eeb145'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'category', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'category', type_='unique')
    # ### end Alembic commands ###
