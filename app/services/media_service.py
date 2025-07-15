from abc import ABC, abstractmethod

from app.services.pipeline_run_service import PipelineRunService
class MediaServiceFile(ABC):
    @abstractmethod
    def process_media_file(media_file: MediaFile, pipeline: PipelineRunService) -> str:
        pass
