from app.services.media_file_service import MediaFileService
from app.services.grayscale_image_step_service import (
    GrayscaleImageStep,
)
from app.services.invert_color_image_step_service import (
    InvertColorsImageStep,
)
from app.services.pipeline_step_service import PipelineStepService
from app.models.media_file_model import MediaType
from app.extractors.image_metadata_extractor import ImageMetadataExtractor


class ImageMediaFileService(MediaFileService):
    @property
    def pipeline_step_factory(self) -> dict[str, type[PipelineStepService]]:
        return {"grayscale": GrayscaleImageStep, "invert": InvertColorsImageStep}

    @property
    def content_types(self) -> dict[MediaType, list[str]]:
        return {MediaType.IMAGE: ["image/jpeg", "image/png", "image/gif"]}

    @property
    def metadata_extractor(self):
        return ImageMetadataExtractor()
