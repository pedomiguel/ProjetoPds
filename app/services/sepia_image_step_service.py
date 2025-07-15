from PIL import Image
from pathlib import Path
from app.services.pipeline_step_service import PipelineStepService
from app.models import MediaFile


class SepiaImageStepService(PipelineStepService):
    def process(self, media_file: MediaFile) -> MediaFile:
        image = Image.open(Path(media_file.data_path)).convert("RGB")
        sepia_image = self.apply_sepia(image)
        return self._save_media_file(
            parent_media_file=media_file, file_data=sepia_image
        )

    def apply_sepia(self, image: Image.Image) -> Image.Image:
        pixels = image.load()
        for y in range(image.height):
            for x in range(image.width):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))
        return image
