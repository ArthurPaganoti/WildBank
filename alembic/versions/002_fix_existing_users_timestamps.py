from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        UPDATE users 
        SET created_at = COALESCE(created_at, now()),
            updated_at = COALESCE(updated_at, now())
        WHERE created_at IS NULL OR updated_at IS NULL;
    """)


def downgrade() -> None:
    pass

