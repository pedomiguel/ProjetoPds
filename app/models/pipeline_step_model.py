import uuid
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, JSON
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import BaseModel
from app.models.pipeline_run_model import PipelineRun


class PipelineStep(BaseModel):
    __tablename__ = "pipeline_steps"

    id: Mapped[uuid.UUID] = mapped_column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    pipeline_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("pipeline_runs.id", ondelete="CASCADE"), nullable=False
    )

    model_key: Mapped[str] = mapped_column(String, nullable=False)
    parameters: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)

    pipeline_run: Mapped["PipelineRun"] = relationship(back_populates="steps")
