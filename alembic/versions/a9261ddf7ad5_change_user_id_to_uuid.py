"""Change user id to UUID

Revision ID: a9261ddf7ad5
Revises: 831ce610c619
Create Date: 2024-04-16 00:43:47.756144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9261ddf7ad5'
down_revision: Union[str, None] = '831ce610c619'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
