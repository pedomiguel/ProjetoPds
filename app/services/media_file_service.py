from abc import ABC, abstractmethod
from pathlib import Path
import shutil
from uuid import uuid4, UUID
from typing import List, Optional
from fastapi import UploadFile, BackgroundTasks
from fastapi.responses import FileResponse

from app.models import MediaFile, MediaType
from app.exceptions import MediaTypeNotSupportedException, NotFoundException
from app.exceptions.unable_to_create_pipeline_exception import (
    UnableToCreatePipelineException,
)
from app.repositories import MediaFileRepository
from app.services.pipeline_run_service import PipelineRunService
from app.services.pipeline_step_service import PipelineStepService
from app.schemas import MediaFileCreate, MediaFileUpdate

from app.extractors.media_metadata_extractor import MediaMetadataExtractor


class MediaFileService(ABC):
    def __init__(self):
        self.repository = MediaFileRepository()

    @property
    @abstractmethod
    def content_types(self) -> dict[MediaType, List[str]]:
        pass

    @property
    @abstractmethod
    def pipeline_step_factory(self) -> dict:
        pass

    @property
    @abstractmethod
    def metadata_extractor(self) -> MediaMetadataExtractor | None:
        pass

    def _validate_upload(self, file: UploadFile, media_type: MediaType) -> None:
        allowed = self.content_types.get(media_type, [])
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
        media = MediaFileCreate(
            id=media_id,
            name=name,
            data_path=path,
            user_id=user_id,
            media_type=media_type,
            parent_id=parent_id,
        )

        return self.repository.create(media)

    def _instantiate_pipeline_step(self, key: str) -> PipelineStepService:
        try:
            factory = self.pipeline_step_factory

            StepClass = factory.get(key)

            print(StepClass)

            if StepClass:
                return StepClass()

            raise NotFoundException(f"Pipeline step '{key}' not found.")
        except NotFoundException as e:
            raise e
        except Exception:
            raise UnableToCreatePipelineException()

    def get_media_type(self, file: UploadFile) -> MediaType:
        for media_type, allowed_types in self.content_types.items():
            if file.content_type in allowed_types:
                return media_type

        raise MediaTypeNotSupportedException(
            f"Unsupported media type: {file.content_type}"
        )

    def upload(
        self,
        file: UploadFile,
        user_id: UUID,
        pipeline: List[str],
        background_tasks: BackgroundTasks,
    ) -> List[MediaFile]:
        media_type = self.get_media_type(file)

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
            steps_instances.append(step)

        runner = PipelineRunService(steps_instances)
        all_media = runner.run(original_media)

        for media in all_media:
            if not media.media_metadata:
                background_tasks.add_task(self._extract_metadata, media)

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
        return self.repository.update(data, media)

    def delete(self, id: UUID) -> MediaFile:
        media = self.find_by_id(id)
        return self.repository.delete(media)

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
        allowed = self.content_types.get(media_type, [])

        return allowed[0] if allowed else "application/octet-stream"

    def _extract_metadata(self, media: MediaFile):
        extractor = self.metadata_extractor

        if not extractor:
            return

        metadata_dict = extractor.extract(Path(media.data_path))

        self.repository.update(
            MediaFileUpdate(
                media_metadata=metadata_dict,
            ),
            media,
        )
