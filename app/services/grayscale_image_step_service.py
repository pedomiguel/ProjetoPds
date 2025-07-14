from pathlib import Path
from PIL import Image

from app.models import MediaFile
from app.services.pipeline_step_service import PipelineStepService


class GrayscaleImageStep(PipelineStepService):
    def process(self, media_file: MediaFile) -> MediaFile:
        original_path = Path(media_file.data_path)
        image = Image.open(original_path).convert("L")

        return self._save_media_file(parent_media_file=media_file, file_data=image)
