from sqlalchemy import String, UUID as SQLAlchemyUUID, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from .base import BaseModel


class Organization(BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String, nullable=False)
    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    billing_email: Mapped[str | None] = mapped_column(String, nullable=True)
    ein: Mapped[str | None] = mapped_column(Text, nullable=True)
    plan: Mapped[str] = mapped_column(String, default="free", nullable=False)

    members: Mapped[List["OrganizationMember"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}')>"
