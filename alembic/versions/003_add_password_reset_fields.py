from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP

revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password_reset_token', sa.String(500), nullable=True))
    op.add_column('users', sa.Column('password_reset_expires', TIMESTAMP(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'password_reset_expires')
    op.drop_column('users', 'password_reset_token')

