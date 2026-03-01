"""add user_session_tokens table

Revision ID: b8f9a7d3e1c4
Revises: 2b031989a2b8
Create Date: 2026-02-16 20:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b8f9a7d3e1c4"
down_revision: Union[str, Sequence[str], None] = "2b031989a2b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_session_tokens",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
        sa.UniqueConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("user_session_tokens")
