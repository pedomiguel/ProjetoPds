import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as pgUUID

from app.config import BaseModel


class UserFollower(BaseModel):
    __tablename__ = "user_followers"

    follower_id: Mapped[uuid.UUID] = mapped_column(
        pgUUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )
    following_id: Mapped[uuid.UUID] = mapped_column(
        pgUUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )

    __table_args__ = (
        UniqueConstraint(
            "follower_id", "following_id", name="unique_follower_following"
        ),
    )
