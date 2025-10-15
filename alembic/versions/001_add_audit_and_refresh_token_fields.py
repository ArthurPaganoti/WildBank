from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('refresh_token', sa.String(length=500), nullable=True))
    op.add_column('users', sa.Column('refresh_token_expires', sa.DateTime(timezone=True), nullable=True))

    op.add_column('users',
                  sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column('users',
                  sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column('users', sa.Column('last_login', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')

    # Remover campos de refresh token
    op.drop_column('users', 'refresh_token_expires')
    op.drop_column('users', 'refresh_token')

