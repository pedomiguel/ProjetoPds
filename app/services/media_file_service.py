import shutil
from uuid import UUID, uuid4
from pathlib import Path
from typing import List

from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.repositories import MediaFileRepository
from app.models import MediaFile, MediaType
from app.schemas.media_file_schema import MediaFileCreate, MediaFileUpdate
from app.exceptions import NotFoundException, MediaTypeNotSupportedException


class MediaFileService:
    __ALLOWED_CONTENT_TYPES = {
        MediaType.AUDIO: [
            "audio/mpeg",
            "audio/wav",
            "audio/ogg",
            "audio/flac",
            "audio/aac",
        ],
        MediaType.VIDEO: [
            "video/mp4",
            "video/webm",
            "video/ogg",
        ],
        MediaType.IMAGE: [
            "image/png",
            "image/jpeg",
            "image/webp",
        ],
    }

    def __init__(self) -> None:
        self.repository = MediaFileRepository()
        # self.inference_facade = MediaInference()

    def find_by_id(self, id: UUID) -> MediaFile:
        media = self.repository.find_by_id(id)
        if not media:
            raise NotFoundException("Media file not found")
        return media

    def get_all(self, user_id: UUID) -> List[MediaFile]:
        medias = self.repository.find_media_by_user_id(user_id)
        if not medias:
            raise NotFoundException("No media files found for this user")
        return medias

    def download(self, id: UUID, user_id: UUID):
        media = self.find_by_id(id)
        if not media or media.user_id != user_id:
            raise NotFoundException("Media file not found.")
        file_path = Path(media.data_path)
        if not file_path.exists():
            raise NotFoundException("Media file not found on disk")
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type="application/octet-stream",
        )

    def update(self, data: MediaFileUpdate, id: UUID) -> MediaFile:
        media = self.find_by_id(id)
        return self.repository.update(data, media)

    def delete(self, id: UUID) -> MediaFile:
        media = self.find_by_id(id)
        return self.repository.delete(media)

    def upload(
        self,
        file: UploadFile,
        user_id: UUID,
        pipeline: List[str],
        media_type: MediaType,
    ) -> MediaFile:
        self._validate_upload(file, pipeline, media_type)

        media_id = uuid4()
        base_dir = Path(f"uploads/{user_id}/{media_id}/")
        base_dir.mkdir(parents=True, exist_ok=True)
        original_file_path = base_dir / file.filename

        with original_file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        original_media = self._create_media_instance(
            media_id, file.filename, str(original_file_path), user_id, media_type
        )

        # current_input_path = base_dir
        # for model_key in pipeline:
        #     current_input_path = self._run_pipeline_step(
        #         model_key, current_input_path, user_id, original_media.id, media_type
        #     )

        return original_media

    def _validate_upload(
        self,
        file: UploadFile,
        pipeline: List[str],
        media_type: MediaType,
    ) -> MediaType:
        allowed_types = self.__ALLOWED_CONTENT_TYPES.get(media_type, [])
        if file.content_type not in allowed_types:
            allowed = ", ".join(allowed_types)
            raise MediaTypeNotSupportedException(
                f"{media_type.value} type not supported. Allowed: {allowed}"
            )

        # for key in pipeline:
        #     if key not in MODEL_CONFIG_MAP:
        #         raise ValueError(f"Unsupported model in pipeline: {key}")

        return media_type

    def _create_media_instance(
        self,
        media_id: UUID,
        name: str,
        path: str,
        user_id: UUID,
        media_type: MediaType,
        parent_id: UUID | None = None,
    ) -> MediaFile:
        return self.repository.create(
            MediaFileCreate(
                id=media_id,
                name=name,
                data_path=path,
                user_id=user_id,
                media_type=media_type,
                parent_id=parent_id,
            )
        )

    def _run_pipeline_step(
        self,
        model_key: str,
        input_path: Path,
        user_id: UUID,
        parent_id: UUID,
        media_type: MediaType,
    ) -> Path:
        return None
        # self.model_downloader.download_model(model_key)
        # outputs = self.inference_facade.pipeline_inference(str(input_path), model_key)

        # for output in outputs:
        #     self._create_media_instance(
        #         uuid4(), output["name"], output["path"], user_id, media_type, parent_id
        #     )

        # return Path(outputs[0]["path"]).parent if outputs else input_path
