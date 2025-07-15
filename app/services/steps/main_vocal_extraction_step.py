from .base_audio_stem_step import BaseAudioStemStep

class MainVocalExtractionStep(BaseAudioStemStep):
    stem_name = "main_vocal"
    model_type = "mel_band_roformer"
    config_path = "app/extractor_app/configs/gabox_melroformer/karaokegabox_1750911344.yaml"
    start_check_point = "app/extractor_app/configs/ckpt/Karaoke_GaboxV1.ckpt" 