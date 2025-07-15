from typing import List

from app.services.pipeline_step_service import PipelineStepService
from app.models.media_file_model import MediaFile


class PipelineRunService:
    def __init__(self, steps: List[PipelineStepService]):
        self.steps = steps

    def run(self, original_media: MediaFile) -> List[MediaFile]:
        all_media = [original_media]
        current_media = original_media

        for step in self.steps:
            try:
                new_media = step.process(current_media)
                all_media.append(new_media)
                current_media = new_media
            except Exception:
                continue

        return all_media
