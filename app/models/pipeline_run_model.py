import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.config import BaseModel
from app.models.media_file_model import MediaFile
from app.models.user_model import User
from app.models.media_file_model import MediaType


class PipelineRun(BaseModel):
    __tablename__ = "pipeline_runs"

    id: Mapped[uuid.UUID] = mapped_column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    media_type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)

    input_file_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("media_files.id", ondelete="SET NULL"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="pipeline_runs")
    input_file: Mapped[Optional["MediaFile"]] = relationship()
    steps: Mapped[List["PipelineStep"]] = relationship(
        back_populates="pipeline_run",
        cascade="all, delete-orphan",
        order_by="PipelineStep.order",
    )
