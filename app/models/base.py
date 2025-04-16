from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import MetaData, DateTime, UUID as SQLAlchemyUUID
from sqlalchemy.sql import func
import uuid as uuid_pkg  # Use alias to avoid conflict with column name
from datetime import datetime

# Optional: Define naming conventions for constraints
# Helps keep index/constraint names consistent and avoids
# potential auto-generation conflicts with Alembic/databases.
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata_obj = MetaData(schema="public", naming_convention=convention)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models with metadata."""

    metadata = metadata_obj


@declared_attr
def id(cls) -> Mapped[uuid_pkg.UUID]:
    return mapped_column(
        SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4
    )


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""

    # Use declared_attr for columns that might need table-specific context
    # although not strictly necessary for these simple defaults.
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )


class SoftDeleteMixin:
    """Mixin for a nullable deleted_at timestamp for soft deletes."""

    @declared_attr
    def deleted_at(cls) -> Mapped[datetime | None]:
        return mapped_column(DateTime(timezone=True), nullable=True, index=True)


# Combine Base and Mixins for common usage if desired, or apply individually
# class BaseModel(Base, TimestampMixin, SoftDeleteMixin):
#     id: Mapped[uuid_pkg.UUID] = mapped_column(
#         SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4
#     )

# Or, more flexible: Keep Base separate and apply mixins as needed
# Let's stick with this approach for now.


# --- Consolidated Base Model ---
class BaseModel(Base, TimestampMixin, SoftDeleteMixin):
    """Consolidated base model including ID, timestamps, and soft delete."""

    # Make this class abstract so SQLAlchemy doesn't try to create a table for it
    __abstract__ = True

    # Define the primary key directly here
    id: Mapped[uuid_pkg.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid_pkg.uuid4
    )
