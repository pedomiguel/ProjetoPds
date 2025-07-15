from app.controllers.media_file_controller import MediaFileController
from app.services.audio_file_service import AudioFileService
from fastapi import BackgroundTasks, File, Form, UploadFile, Depends, HTTPException
from app.dependencies import AuthGuard
from app.schemas.media_file_schema import MediaFileSingleResponse
from app.models import User
from typing import List

class AudioFileController(MediaFileController):
    @property
    def media_service(self):
        return AudioFileService() 