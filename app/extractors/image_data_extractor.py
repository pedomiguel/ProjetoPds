from PIL import Image


from app.extractors.media_extraction_strategy import MediaExtractionStrategy


class ImageDataExtractor(MediaExtractionStrategy):
    def extract(self, file_path: str) -> dict:
        try:
            with Image.open(file_path) as img:
                return {
                    "format": img.format,
                    "mode": img.mode,
                    "size": {"width": img.width, "height": img.height},
                }
        except Exception:
            return {
                "format": None,
                "mode": None,
                "size": {"width": None, "height": None},
            }
