from pathlib import Path
from typing import List
from uuid import UUID

from app.services.pipeline_step_service import PipelineStepService
from app.models.media_file_model import MediaFile


class PipelineRunService:
    def __init__(self, steps: List[PipelineStepService]):
        self.steps = steps

    def run(self, original_media: MediaFile, user_id: UUID) -> List[MediaFile]:
        all_media = [original_media]
        current_media = original_media

        for step in self.steps:
            new_media = step.process(current_media, user_id)
            all_media.append(new_media)
            current_media = new_media

        return all_media
