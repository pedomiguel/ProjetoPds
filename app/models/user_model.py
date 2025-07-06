import uuid
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as pgUUID

from app.config import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    following: Mapped[List["User"]] = relationship(
        "User",
        secondary="user_followers",
        primaryjoin="User.id == UserFollower.follower_id",
        secondaryjoin="User.id == UserFollower.following_id",
        back_populates="followers",
    )

    followers: Mapped[List["User"]] = relationship(
        "User",
        secondary="user_followers",
        primaryjoin="User.id == UserFollower.following_id",
        secondaryjoin="User.id == UserFollower.follower_id",
        back_populates="following",
    )

    media_files: Mapped[List["MediaFile"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    posts: Mapped[List["Post"]] = relationship(  # pyright: ignore
        back_populates="author", cascade="all, delete"
    )
