"""Final Migration1

Revision ID: 6c9d27fb2ec7
Revises: 
Create Date: 2024-06-13 18:55:20.056050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c9d27fb2ec7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ProfilePhoto', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'ProfilePhoto', 'Users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ProfilePhoto', type_='foreignkey')
    op.drop_column('ProfilePhoto', 'user_id')
    # ### end Alembic commands ###
