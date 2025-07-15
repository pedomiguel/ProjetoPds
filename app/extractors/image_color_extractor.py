from colorthief import ColorThief
from app.extractors.media_extraction_strategy import MediaExtractionStrategy


class ImageColorExtractor(MediaExtractionStrategy):
    def extract(self, file_path: str) -> dict:
        try:
            color_thief = ColorThief(file_path)
            dominant_color = color_thief.get_color(quality=1)

            return {"dominant_color": dominant_color}
        except Exception:
            return {"dominant_color": None}
