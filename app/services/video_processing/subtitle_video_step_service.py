import os
from pathlib import Path
import whisper
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

from app.models import MediaFile
from app.services.pipeline_run_service import PipelineStepService

class SubtitleVideoStep(PipelineStepService):
    def process(self, media_file: MediaFile) -> MediaFile:
        video_path = media_file.data_path
        audio_path = f"{media_file}_audio.wav"

        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)

        width, height = video.size

        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        os.remove(audio_path)

        subtitles = []
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            text_clip = (
                TextClip(text=text, font_size=24, color="white", method="caption", size=(width, 100))
                .with_position("center", "bottom")
                .with_start(start)
                .with_duration(end - start)
            )
            subtitles.append(text_clip)

        subtitle_video = CompositeVideoClip([video, *subtitles])
        output_path = Path(video_path).with_name(f"{Path(video_path).stem}_subtilte.mp4")

        subtitle_video.write_videofile(str(output_path), codec="libx264", audio_codec="aac")

        return self._save_media_file(media_file, output_path)
