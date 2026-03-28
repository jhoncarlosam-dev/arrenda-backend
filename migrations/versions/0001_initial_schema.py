"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-03-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            sa.Enum("ARRENDADOR", "ARRENDATARIO", name="roleenum"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "contracts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("arrendador_id", sa.Integer(), nullable=False),
        sa.Column("arrendatario_id", sa.Integer(), nullable=False),
        sa.Column("direccion", sa.String(length=255), nullable=False),
        sa.Column("tipo", sa.String(length=100), nullable=False),
        sa.Column("valor", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("servicios", sa.Text(), nullable=True),
        sa.Column("clausulas_opcionales", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["arrendador_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["arrendatario_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contracts_id"), "contracts", ["id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_contracts_id"), table_name="contracts")
    op.drop_table("contracts")

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS roleenum")
