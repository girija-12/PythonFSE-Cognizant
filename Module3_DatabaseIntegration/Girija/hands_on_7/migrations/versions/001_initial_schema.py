from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None
def upgrade():
    op.create_table(
        "departments",
        sa.Column("department_id", sa.Integer(), primary_key=True),
        sa.Column("dept_name", sa.String(100), nullable=False),
        sa.Column("head_of_dept", sa.String(100)),
        sa.Column("budget", sa.Numeric(12, 2))
    )
    op.create_table(
        "students",
        sa.Column("student_id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(50)),
        sa.Column("last_name", sa.String(50)),
        sa.Column("email", sa.String(100), unique=True),
        sa.Column("date_of_birth", sa.Date()),
        sa.Column("department_id", sa.Integer(), sa.ForeignKey("departments.department_id")),
        sa.Column("enrollment_year", sa.Integer())
    )
    op.create_table(
        "courses",
        sa.Column("course_id", sa.Integer(), primary_key=True),
        sa.Column("course_name", sa.String(150)),
        sa.Column("course_code", sa.String(20), unique=True),
        sa.Column("credits", sa.Integer())
    )
    op.create_table(
        "professors",
        sa.Column("professor_id", sa.Integer(), primary_key=True),
        sa.Column("prof_name", sa.String(100)),
        sa.Column("email", sa.String(100), unique=True),
        sa.Column("salary", sa.Numeric(10, 2))
    )
    op.create_table(
        "enrollments",
        sa.Column("enrollment_id", sa.Integer(), primary_key=True),
        sa.Column("student_id", sa.Integer(), sa.ForeignKey("students.student_id")),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.course_id"))
    )

def downgrade():
    op.drop_table("enrollments")
    op.drop_table("professors")
    op.drop_table("courses")
    op.drop_table("students")
    op.drop_table("departments")