from app.services.media_file_service import MediaFileService
from app.models import MediaType
from app.services.steps.vocal_extraction_step import VocalExtractionStep
from app.services.steps.instrumental_extraction_step import InstrumentalExtractionStep
from app.services.steps.main_vocal_extraction_step import MainVocalExtractionStep
from app.services.steps.backing_vocal_extraction_step import BackingVocalExtractionStep
from app.services.steps.vocal_enhancement_step import VocalEnhancementStep
from app.repositories import PipelineRunRepository, PipelineStepRepository
from app.schemas.pipeline_run_schema import PipelineRunCreate
from app.schemas.pipeline_step_schema import PipelineStepCreate
from app.services.pipeline_run_service import PipelineRunService
from pathlib import Path
import shutil
from uuid import uuid4
import os

class AudioFileService(MediaFileService):
    @property
    def content_types(self):
        return {MediaType.AUDIO: ["audio/wav", "audio/mpeg", "audio/mp3"]}

    @property
    def pipeline_step_factory(self):
        return {
            "vocal_extraction": VocalExtractionStep,
            "instrumental_extraction": InstrumentalExtractionStep,
            "main_vocal_extraction": MainVocalExtractionStep,
            "backing_vocal_extraction": BackingVocalExtractionStep,
            "vocal_enhancement": VocalEnhancementStep,
        }

    @property
    def metadata_extractor(self):
        # Placeholder: implement or inject your audio metadata extractor here
        return None