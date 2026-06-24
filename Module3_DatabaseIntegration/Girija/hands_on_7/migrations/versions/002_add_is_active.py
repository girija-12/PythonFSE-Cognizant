from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
def upgrade():
    op.add_column(
        "students",
        sa.Column("is_active", sa.Boolean(), nullable=True, server_default="1")
    )
def downgrade():
    op.drop_column("students", "is_active")