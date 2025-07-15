from pathlib import Path

from PIL import Image, ImageFilter

from app.models import MediaFile
from app.services.pipeline_step_service import PipelineStepService


class EdgeDetectImageStepService(PipelineStepService):
    def process(self, media_file: MediaFile) -> MediaFile:
        try:
            image = Image.open(Path(media_file.data_path))
            edged = image.filter(ImageFilter.FIND_EDGES)

            return self._save_media_file(parent_media_file=media_file, file_data=edged)
        except Exception:
            return media_file
