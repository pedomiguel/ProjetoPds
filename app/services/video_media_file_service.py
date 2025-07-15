from app.extractors.video_metadata_extractor import VideoMetadataExtractor
from app.models.media_file_model import MediaType
from app.services.media_file_service import MediaFileService
from app.services.video_processing import SubtitleVideoStep
from app.extractors import MediaMetadataExtractor

class VideoMediaFileService(MediaFileService):
    @property
    def pipeline_step_factory(self) -> dict:
        return {"subtitles": SubtitleVideoStep, }

    @property
    def metadata_extractor(self) -> MediaMetadataExtractor:
        return VideoMetadataExtractor

    @property
    def content_types(self) -> dict[MediaType, list[str]]:
        return {MediaType.VIDEO: ["video/mp4"]}
