"""empty message

Revision ID: d3b64e3273ee
Revises: f9a0693d9171
Create Date: 2024-04-18 14:29:19.415514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3b64e3273ee'
down_revision: Union[str, None] = 'f9a0693d9171'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'test')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('test', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###