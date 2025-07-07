from abc import ABC, abstractmethod
from uuid import UUID
from fastapi import Depends, File, UploadFile, Form, BackgroundTasks
from typing import List

from app.dependencies import AuthGuard
from app.services.media_file_service import MediaFileService
from app.schemas.media_file_schema import (
    MediaFileUpdate,
    MediaFileSingleResponse,
    MediaFileParentResponse,
)
from app.models import User
from .controller import BaseController


class MediaFileController(BaseController, ABC):
    def __init__(self, prefix: str = "/media", tags: list[str] = ["Media"]):
        super().__init__(tags=tags, prefix=prefix)

    @property
    @abstractmethod
    def media_service(self) -> MediaFileService:
        raise NotImplementedError()

    def add_routes(self) -> None:
        @self.router.get("/", response_model=List[MediaFileParentResponse])
        def get_all(user: User = Depends(AuthGuard.get_authenticated_user)):
            medias = self.media_service.get_all(user.id)
            return [MediaFileParentResponse.model_validate(media) for media in medias]

        @self.router.post("/upload", response_model=List[MediaFileSingleResponse])
        def upload(
            background_tasks: BackgroundTasks,
            file: UploadFile = File(...),
            pipeline: str = Form(...),
            user: User = Depends(AuthGuard.get_authenticated_user),
        ):
            pipeline_list = [p.strip() for p in pipeline.split(",") if p.strip()]
            media_list = self.media_service.upload(
                file, user.id, pipeline_list, background_tasks
            )
            return [
                MediaFileSingleResponse.model_validate(media) for media in media_list
            ]

        @self.router.get("/download/{id}")
        def download(id: UUID, user: User = Depends(AuthGuard.get_authenticated_user)):
            return self.media_service.download(id, user.id)

        @self.router.put("/update/{id}")
        def update(
            id: UUID,
            data: MediaFileUpdate,
            _: User = Depends(AuthGuard.get_authenticated_user),
        ):
            media_updated = self.media_service.update(data, id)
            return MediaFileSingleResponse.model_validate(media_updated)

        @self.router.delete("/delete/{id}", status_code=204)
        def delete(id: UUID, _: User = Depends(AuthGuard.get_authenticated_user)):
            media_deleted = self.media_service.delete(id)
            return MediaFileSingleResponse.model_validate(media_deleted)
