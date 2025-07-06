from abc import ABC, abstractmethod
from pathlib import Path
import shutil
from uuid import uuid4, UUID
from typing import List, Optional
from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.models import MediaFile, MediaType
from app.exceptions import MediaTypeNotSupportedException, NotFoundException
from app.repositories import MediaFileRepository
from app.services.pipeline_run_service import PipelineRunService
from app.services.pipeline_step_service import PipelineStepService


class MediaFileService(ABC):
    __ALLOWED_CONTENT_TYPES = {
        MediaType.AUDIO: [
            "audio/mpeg",
            "audio/wav",
            "audio/ogg",
            "audio/flac",
            "audio/aac",
        ],
        MediaType.VIDEO: ["video/mp4", "video/avi", "video/mkv"],
        MediaType.IMAGE: ["image/jpeg", "image/png", "image/gif"],
    }

    def __init__(self):
        self.repository = MediaFileRepository()

    def _validate_upload(self, file: UploadFile, media_type: MediaType) -> None:
        allowed = self.get_allowed_content_types().get(media_type, [])
        if file.content_type not in allowed:
            allowed_str = ", ".join(allowed)
            raise MediaTypeNotSupportedException(
                f"{media_type.value} type not supported. Allowed types: {allowed_str}"
            )

    def _create_media_instance(
        self,
        media_id: UUID,
        name: str,
        path: str,
        user_id: UUID,
        media_type: MediaType,
        parent_id: Optional[UUID] = None,
    ) -> MediaFile:

        media = MediaFile(
            id=media_id,
            name=name,
            data_path=path,
            user_id=user_id,
            media_type=media_type,
            parent_id=parent_id,
        )
        return self.repository.create(media)

    @abstractmethod
    def get_allowed_content_types(self) -> dict[MediaType, List[str]]:
        return self.__ALLOWED_CONTENT_TYPES

    @abstractmethod
    def get_pipeline_step_factory(self) -> dict[str, type[PipelineStepService]]:
        pass

    def _instantiate_pipeline_step(self, key: str) -> Optional[PipelineStepService]:
        factory = self.get_pipeline_step_factory()
        StepClass = factory.get(key)
        if StepClass:
            return StepClass()
        return None

    def upload(
        self,
        file: UploadFile,
        user_id: UUID,
        pipeline: List[str],
        media_type: MediaType,
    ) -> List[MediaFile]:
        self._validate_upload(file, media_type)

        media_id = uuid4()
        base_dir = Path(f"uploads/{user_id}/{media_id}/")
        base_dir.mkdir(parents=True, exist_ok=True)

        original_file_path = base_dir / file.filename

        with original_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        original_media = self._create_media_instance(
            media_id=media_id,
            name=file.filename,
            path=str(original_file_path),
            user_id=user_id,
            media_type=media_type,
        )

        steps_instances = []
        for key in pipeline:
            step = self._instantiate_pipeline_step(key)
            if step:
                steps_instances.append(step)

        runner = PipelineRunService(steps_instances)
        all_media = runner.run(original_media, user_id)

        return all_media

    def get_all(self, user_id: UUID) -> List[MediaFile]:
        medias = self.repository.find_media_by_user_id(user_id)
        if not medias:
            raise NotFoundException("No media files found for this user.")
        return medias

    def find_by_id(self, id: UUID) -> MediaFile:
        media = self.repository.find_by_id(id)
        if not media:
            raise NotFoundException("Media file not found.")
        return media

    def update(self, data: dict, id: UUID) -> MediaFile:
        media = self.find_by_id(id)
        for key, value in data.items():
            if hasattr(media, key):
                setattr(media, key, value)
        self.repository.db.commit()
        self.repository.db.refresh(media)
        return media

    def delete(self, id: UUID) -> MediaFile:
        media = self.find_by_id(id)
        self.repository.delete(media)
        return media

    def download(self, id: UUID, user_id: UUID) -> FileResponse:
        media = self.find_by_id(id)
        if media.user_id != user_id:
            raise NotFoundException("Media file not found.")
        file_path = Path(media.data_path)
        if not file_path.exists():
            raise NotFoundException("Media file not found on disk.")
        media_type_mime = self._get_mime_type(media.media_type)
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type=media_type_mime,
        )

    def _get_mime_type(self, media_type: MediaType) -> str:
        allowed = self.get_allowed_content_types().get(media_type, [])

        return allowed[0] if allowed else "application/octet-stream"
