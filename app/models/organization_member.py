from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from .base import BaseModel
from .organization import Organization
from .user import User


class OrganizationMember(BaseModel):
    __tablename__ = "organization_members"

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="organizations")

    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "organization_id", name="uq_organization_members_organization_id"
        ),  # Assuming you want to keep this unique constraint
    )

    def __repr__(self) -> str:
        return f"<OrganizationMember(org_id={self.organization_id}, user_id={self.user_id})>"
