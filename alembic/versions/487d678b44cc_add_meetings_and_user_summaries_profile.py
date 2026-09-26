"""add meetings and user summaries, profile

Revision ID: 487d678b44cc
Revises: 367bfc151786
Create Date: 2026-09-25 19:52:43.761813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "487d678b44cc"
down_revision: Union[str, Sequence[str], None] = "367bfc151786"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "meetings",
        sa.Column(
            "meeting_id",
            sa.Uuid(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "summary",
            sa.Text(),
            server_default="",
            nullable=False,
        ),
        sa.Column(
            "start",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "finish",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("meeting_id"),
    )

    op.add_column(
        "conversations",
        sa.Column("meeting_id", sa.Uuid(), nullable=False),
    )

    op.add_column(
        "conversations",
        sa.Column(
            "summary",
            sa.Text(),
            server_default="",
            nullable=False,
        ),
    )

    op.create_foreign_key(
        "fk_conversation_meeting_id",
        "conversations",
        "meetings",
        ["meeting_id"],
        ["meeting_id"],
    )

    op.add_column(
        "users",
        sa.Column(
            "profile",
            sa.Text(),
            server_default="",
            nullable=False,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "summary",
            sa.Text(),
            server_default="",
            nullable=False,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "last_interaction_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
    )

    op.create_unique_constraint(
        "uq_users_username",
        "users",
        ["username"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_users_username",
        "users",
        type_="unique",
    )

    op.drop_column("users", "last_interaction_at")
    op.drop_column("users", "summary")
    op.drop_column("users", "profile")

    op.drop_constraint(
        "fk_conversation_meeting_id",
        "conversations",
        type_="foreignkey",
    )

    op.drop_column("conversations", "summary")
    op.drop_column("conversations", "meeting_id")

    op.drop_table("meetings")