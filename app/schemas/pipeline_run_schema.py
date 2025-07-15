from uuid import UUID
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.models.media_file_model import MediaType
from app.schemas.pipeline_step_schema import PipelineStepCreate, PipelineStepResponse


class PipelineRunCreate(BaseModel):
    user_id: UUID
    media_type: MediaType
    input_file_id: Optional[UUID] = None
    steps: List[PipelineStepCreate]


class PipelineRunResponse(BaseModel):
    id: UUID
    media_type: MediaType
    created_at: datetime
    input_file_id: Optional[UUID]
    steps: List[PipelineStepResponse]

    model_config = ConfigDict(from_attributes=True)
