from app.models.media_file_model import MediaType
from app.services.media_file_service import MediaFileService
from app.services.video_processing import SubtitleVideoStep, SpeedUpVideoStep, InvertGrayVideoStep
from app.extractors import MediaMetadataExtractor

from app.extractors.video_data_extractor import VideoDataExtractor


class VideoMediaFileService(MediaFileService):
    @property
    def pipeline_step_factory(self) -> dict:
        return {"subtitles": SubtitleVideoStep, "speedup": SpeedUpVideoStep, "inverted": InvertGrayVideoStep}

    @property
    def metadata_extractor(self):
        return MediaMetadataExtractor(strategies=[VideoDataExtractor()])

    @property
    def content_types(self) -> dict[MediaType, list[str]]:
        return {MediaType.VIDEO: ["video/mp4"]}
