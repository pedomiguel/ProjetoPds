from app.controllers.media_file_controller import MediaFileController
from app.services.image_media_file_service import ImageMediaFileService
from app.services.media_file_service import MediaFileService


class ImageMediaFileController(MediaFileController):
    def __init__(self):
        super().__init__(tags=["Image Media"], prefix="/image")

    @property
    def media_service(self) -> MediaFileService:
        return ImageMediaFileService()
