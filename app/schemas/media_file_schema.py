from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.models import MediaType


class MediaFileCreate(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    data_path: str
    media_type: MediaType
    parent_id: Optional[UUID] = None


class MediaFileUpdate(BaseModel):
    name: Optional[str] = None
    pinned: Optional[bool] = None


class MediaFilePost(BaseModel):
    id: UUID
    name: str
    media_type: MediaType
    date_in: datetime
    data_path: str
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)


class MediaFileSingleResponse(BaseModel):
    id: UUID
    name: str
    media_type: MediaType
    date_in: datetime
    data_path: str
    date_modified: datetime
    parent_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)


class MediaFileParentResponse(BaseModel):
    id: UUID
    name: str
    media_type: MediaType
    date_in: datetime
    data_path: str
    date_modified: datetime
    children: List[MediaFileSingleResponse]

    model_config = ConfigDict(from_attributes=True)
