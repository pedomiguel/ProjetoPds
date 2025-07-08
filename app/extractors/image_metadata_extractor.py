from PIL import Image

from .media_metadata_extractor import MediaMetadataExtractor


class ImageMetadataExtractor(MediaMetadataExtractor):
    def extract(self, file_path: str) -> dict:
        with Image.open(file_path) as img:
            metadata = {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "info": img.info,
            }

        return metadata
