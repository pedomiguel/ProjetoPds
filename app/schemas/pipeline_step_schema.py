from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PipelineStepCreate(BaseModel):
    model_key: str
    parameters: dict | None = None
    order: int


class PipelineStepResponse(BaseModel):
    id: UUID
    model_key: str
    parameters: Optional[dict]
    order: int

    model_config = ConfigDict(from_attributes=True)
