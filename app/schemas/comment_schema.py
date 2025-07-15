from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

from app.schemas import UserBase


class CommentResponse(BaseModel):
    id: UUID
    content: str
    author: UserBase
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    content: str
    post_id: UUID
    author_id: UUID


class CommentUpdate(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)


class CommentCreateRequest(BaseModel):
    content: str
