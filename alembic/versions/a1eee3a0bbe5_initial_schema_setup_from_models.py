"""Initial schema setup from models

Revision ID: a1eee3a0bbe5
Revises:
Create Date: 2025-04-15 01:49:05.530987

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a1eee3a0bbe5"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "organizations",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("website_url", sa.Text(), nullable=True),
        sa.Column("billing_email", sa.String(), nullable=True),
        sa.Column("ein", sa.Text(), nullable=True),
        sa.Column("plan", sa.String(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_organizations")),
        schema="public",
    )
    with op.batch_alter_table("organizations", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_public_organizations_deleted_at"),
            ["deleted_at"],
            unique=False,
        )

    op.create_table(
        "users",
        sa.Column("clerk_id", sa.Text(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("avatar_url", sa.Text(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        schema="public",
    )
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_public_users_clerk_id"), ["clerk_id"], unique=True
        )
        batch_op.create_index(
            batch_op.f("ix_public_users_deleted_at"), ["deleted_at"], unique=False
        )

    op.create_table(
        "organization_members",
        sa.Column("organization_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["public.organizations.id"],
            name=op.f("fk_organization_members_organization_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["public.users.id"],
            name=op.f("fk_organization_members_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_organization_members")),
        sa.UniqueConstraint(
            "organization_id", name="uq_organization_members_organization_id"
        ),
        schema="public",
    )
    with op.batch_alter_table("organization_members", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_public_organization_members_deleted_at"),
            ["deleted_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_public_organization_members_user_id"),
            ["user_id"],
            unique=False,
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("organization_members", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_public_organization_members_user_id"))
        batch_op.drop_index(batch_op.f("ix_public_organization_members_deleted_at"))

    op.drop_table("organization_members", schema="public")
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_public_users_deleted_at"))
        batch_op.drop_index(batch_op.f("ix_public_users_clerk_id"))

    op.drop_table("users", schema="public")
    with op.batch_alter_table("organizations", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_public_organizations_deleted_at"))

    op.drop_table("organizations", schema="public")
