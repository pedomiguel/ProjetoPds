import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, String, TIMESTAMP, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as pgUUID
import enum

from app.config import BaseModel


class MediaType(enum.Enum):
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"
    IMAGE = "IMAGE"


class MediaFile(BaseModel):
    __tablename__ = "media_files"

    id: Mapped[uuid.UUID] = mapped_column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_in: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    date_modified: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    data_path: Mapped[str] = mapped_column(String, nullable=False)
    pinned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    media_type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    owner: Mapped["User"] = relationship(back_populates="media_files")
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        pgUUID(as_uuid=True),
        ForeignKey("media_files.id", ondelete="CASCADE"),
        nullable=True,
    )
    parent: Mapped[Optional["MediaFile"]] = relationship(
        "MediaFile",
        remote_side="MediaFile.id",
        foreign_keys=[parent_id],
        back_populates="children",
    )

    children: Mapped[List["MediaFile"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )

    posts: Mapped[List["Post"]] = relationship(
        secondary="post_media",
        back_populates="media_files",
    )
