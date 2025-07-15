from moviepy import VideoFileClip
from pathlib import Path

from app.extractors.media_metadata_extractor import MediaMetadataExtractor

class VideoMetadataExtractor(MediaMetadataExtractor):
    def extract(self, file_path: Path) -> dict:
        try:
            video = VideoFileClip(file_path)
            return {
                "duration": video.duration,
                "size": video.size,
                "fps": video.fps
            }
        except Exception:
            return {
                "duration": None,
                "size": None,
                "fps": None
            }
