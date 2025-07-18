from pathlib import Path
from moviepy import VideoFileClip, vfx
from moviepy.video.fx import MultiplySpeed

from app.models import MediaFile
from app.services.pipeline_run_service import PipelineStepService

class SpeedUpVideoStep(PipelineStepService):
    def process(self, media_file: MediaFile) -> MediaFile:
        video_path = media_file.data_path
        output_path = Path(video_path).with_name(f"{Path(video_path).stem}_1.5x.mp4")

        video = VideoFileClip(video_path)

        speed_up = MultiplySpeed(factor=1.5).apply(video)

        speed_up.write_videofile(str(output_path), codec="libx264", audio_codec="aac")

        return self._save_media_file(media_file, output_path)
