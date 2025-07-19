from pathlib import Path
from moviepy import VideoFileClip
from moviepy.video.fx import InvertColors

from app.models import MediaFile
from app.services.pipeline_run_service import PipelineStepService

class InvertGrayVideoStep(PipelineStepService):
    def process(self, media_file: MediaFile) -> MediaFile:
        video_path = media_file.data_path
        video = VideoFileClip(video_path)

        processed_video = InvertColors().apply(video)

        output_path = Path(video_path).with_name(f"{Path(video_path).stem}_inverted.mp4")
        processed_video.write_videofile(str(output_path), codec="libx264", audio_codec="aac")

        return self._save_media_file(media_file, output_path)
