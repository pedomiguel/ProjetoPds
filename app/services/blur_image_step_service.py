from pathlib import Path

from PIL import Image, ImageFilter

from app.models import MediaFile
from app.services.pipeline_step_service import PipelineStepService


class BlurImageStepService(PipelineStepService):
    def process(self, media_file: MediaFile) -> MediaFile:
        try:
            image = Image.open(Path(media_file.data_path))
            blurred = image.filter(ImageFilter.GaussianBlur(radius=2))
            return self._save_media_file(
                parent_media_file=media_file, file_data=blurred
            )
        except Exception:
            return media_file
