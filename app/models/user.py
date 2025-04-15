from sqlalchemy import String, UUID as SQLAlchemyUUID, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    clerk_id: Mapped[str] = mapped_column(Text, unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationship to OrganizationMember
    organizations: Mapped[List["OrganizationMember"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
