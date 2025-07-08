from pathlib import Path
from uuid import UUID
from PIL import Image, ImageOps

from app.models import MediaFile
from app.services.pipeline_step_service import PipelineStepService


class GrayscaleImageStep(PipelineStepService):
    def process(self, media_file: MediaFile, user_id: UUID) -> MediaFile:
        original_path = Path(media_file.data_path)
        image = Image.open(original_path).convert("L")  # Convert to grayscale

        output_dir = original_path.parent / "grayscale"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_name = f"{original_path.stem}_grayscale{original_path.suffix}"
        output_path = output_dir / output_name

        image.save(output_path)

        child = self._create_child_media_file(
            name=output_name,
            path=str(output_path),
            user_id=user_id,
            media_type=media_file.media_type,
            parent_id=media_file.id,
        )

        return child


class InvertColorsImageStep(PipelineStepService):
    def process(self, media_file: MediaFile, user_id: UUID) -> MediaFile:
        original_path = Path(media_file.data_path)
        image = Image.open(original_path).convert("RGB")
        inverted_image = ImageOps.invert(image)

        output_dir = original_path.parent / "inverted"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_name = f"{original_path.stem}_inverted{original_path.suffix}"
        output_path = output_dir / output_name

        inverted_image.save(output_path)

        child = self._create_child_media_file(
            name=output_name,
            path=str(output_path),
            user_id=user_id,
            media_type=media_file.media_type,
            parent_id=media_file.id,
        )

        return child
