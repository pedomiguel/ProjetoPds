from .base_audio_stem_step import BaseAudioStemStep

class VocalEnhancementStep(BaseAudioStemStep):
    stem_name = "vocal_enhanced"
    model_type = "mel_band_roformer"
    config_path = "app/extractor_app/configs/gabox_melroformer/voc_gabox.yaml"
    start_check_point = "app/extractor_app/configs/ckpt/voc_fv5.ckpt" 