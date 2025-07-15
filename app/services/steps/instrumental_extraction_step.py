from .base_audio_stem_step import BaseAudioStemStep

class InstrumentalExtractionStep(BaseAudioStemStep):
    stem_name = "instrumental"
    model_type = "mel_band_roformer"
    config_path = "app/extractor_app/configs/gabox_melroformer/inst_gabox.yaml"
    start_check_point = "app/extractor_app/configs/ckpt/voc_fv5.ckpt" 