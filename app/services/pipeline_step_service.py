from uuid import uuid4, UUID
from typing import Optional

from app.models import MediaFile, MediaType
from app.schemas import MediaFileCreate
from app.repositories import MediaFileRepository


class PipelineStepService:
    def __init__(self):
        self.repository = MediaFileRepository()

    def process(self, media_file: MediaFile, user_id: UUID) -> list[MediaFile]:
        raise NotImplementedError("Must implement process method")

    def _create_child_media_file(
        self,
        name: str,
        path: str,
        user_id: UUID,
        media_type: MediaType,
        parent_id: Optional[UUID] = None,
    ) -> MediaFile:
        child = MediaFileCreate(
            id=uuid4(),
            name=name,
            data_path=path,
            user_id=user_id,
            media_type=media_type,
            parent_id=parent_id,
        )

        return self.repository.create(child)
