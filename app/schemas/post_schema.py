from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from typing import List, Optional
from uuid import UUID

from app.schemas.media_file_schema import MediaFilePost
from app.schemas.user_schema import UserBase
from app.schemas.comment_schema import CommentResponse


class PostCreateRequest(BaseModel):
    title: str
    theme: str
    description: Optional[str] = None
    audio_ids: List[UUID] = Field(default_factory=list)
    pipeline_template: Optional[List[str]] = None


class PostCreate(PostCreateRequest):
    author_id: UUID


class PostUpdate(BaseModel):
    title: Optional[str] = None
    theme: Optional[str] = None
    description: Optional[str] = None
    pipeline_template: Optional[List[str]] = None
    audio_ids: Optional[List[UUID]] = None


class PostAuthor(UserBase):
    is_following: bool = False

    model_config = ConfigDict(from_attributes=True)


class PostResponse(BaseModel):
    id: UUID
    title: str
    theme: str
    description: Optional[str]
    pipeline_template: Optional[List[str]]
    files: List[MediaFilePost] = []
    author: PostAuthor
    comments: List[CommentResponse] = []

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
