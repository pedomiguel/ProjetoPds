from app.controllers.media_file_controller import MediaFileController
from app.services.video_media_file_service import VideoMediaFileService
from app.services.media_file_service import MediaFileService

class VideoMediaFileController(MediaFileController):
    def __init__(self, ):
        super().__init__(tags=["Video Media"], prefix="/video")

    @property
    def media_service(self) -> MediaFileService:
        return VideoMediaFileService()
