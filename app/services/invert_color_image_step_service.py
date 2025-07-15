from pathlib import Path

from PIL import Image, ImageOps

from app.models import MediaFile
from app.services.pipeline_step_service import PipelineStepService


class InvertColorsImageStep(PipelineStepService):
    def process(self, media_file: MediaFile) -> MediaFile:
        try:
            original_path = Path(media_file.data_path)
            image = Image.open(original_path).convert("RGB")
            inverted = ImageOps.invert(image)

            return self._save_media_file(
                parent_media_file=media_file, file_data=inverted
            )
        except Exception:
            return media_file
