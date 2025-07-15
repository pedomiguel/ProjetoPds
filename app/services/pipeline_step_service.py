from abc import ABC, abstractmethod

from uuid import uuid4, UUID
from typing import Optional, Union
from pathlib import Path
from datetime import datetime
from PIL import Image
import shutil

from app.models import MediaFile, MediaType
from app.schemas import MediaFileCreate
from app.repositories import MediaFileRepository


class PipelineStepService(ABC):
    def __init__(self):
        self.repository = MediaFileRepository()

    @abstractmethod
    def process(self, media_file: MediaFile) -> MediaFile:
        pass

    def _create_media_file(
        self,
        name: str,
        path: str,
        user_id: UUID,
        media_type: MediaType,
        parent_id: Optional[UUID] = None,
    ) -> MediaFile:
        return self.repository.create(
            MediaFileCreate(
                id=uuid4(),
                name=name,
                data_path=path,
                user_id=user_id,
                media_type=media_type,
                parent_id=parent_id,
            )
        )

    def _save_media_file(
        self,
        parent_media_file: MediaFile,
        file_data: Union[Image.Image, Path, bytes],
    ) -> MediaFile:
        original_path = Path(parent_media_file.data_path)

        timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S")
        output_name = f"{original_path.stem}{timestamp}{original_path.suffix}"
        output_path = original_path.parent / output_name

        if isinstance(file_data, Image.Image):
            file_data.save(output_path)
        elif isinstance(file_data, Path):
            shutil.copy(file_data, output_path)
        elif isinstance(file_data, bytes):
            with open(output_path, "wb") as f:
                f.write(file_data)
        else:
            raise ValueError("Unsupported file_data type")

        return self._create_media_file(
            name=output_name,
            path=str(output_path),
            user_id=parent_media_file.user_id,
            media_type=parent_media_file.media_type,
            parent_id=parent_media_file.id,
        )
