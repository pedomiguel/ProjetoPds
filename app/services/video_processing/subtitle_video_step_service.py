import os
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

        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        os.remove(audio_path)

        subtitles = []
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            text_clip = (
                TextClip(text, font_size=24, color='white', bg_color='black', font='Arial')
                .with_position("centet", "bottom")
                .with_stat(start)
                .with_duration(end - start)
            )
            subtitles.append(text_clip)

        subtitle_video = CompositeVideoClip([video, *subtitles])
        final = subtitle_video.write_videofile(f"{video_path}_subtilte.mp4", codec="libx264", audio_codec="aac")

        return self._save_media_file(media_file, final)
