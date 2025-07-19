from app.controllers.media_file_controller import MediaFileController
from app.services.audio_file_service import AudioFileService
from fastapi import BackgroundTasks, File, Form, UploadFile, Depends, HTTPException
from app.dependencies import AuthGuard
from app.schemas.media_file_schema import MediaFileSingleResponse
from app.schemas import PostCreateRequest, CommentCreate
from app.models import User
from typing import List

class AudioFileController(MediaFileController):
    def __init__(self, tags: list = [], prefix: str = "") -> None:
        super().__init__(tags=["Audio"], prefix="/audio")
        self._media_service = None

    @property
    def media_service(self):
        return AudioFileService()

