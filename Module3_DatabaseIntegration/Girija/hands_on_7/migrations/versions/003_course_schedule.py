from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"

def upgrade():
    op.create_table(
        "course_schedules",
        sa.Column("schedule_id", sa.Integer(), primary_key=True),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("day_of_week", sa.String(20)),
        sa.Column("start_time", sa.Time()),
        sa.Column("end_time", sa.Time()),
        sa.ForeignKeyConstraint(["course_id"], ["courses.course_id"])
    )

def downgrade():
    op.drop_table("course_schedules")