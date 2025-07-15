from app.extractors.media_extraction_strategy import MediaExtractionStrategy


class MediaMetadataExtractor:
    def __init__(self, strategies: list[MediaExtractionStrategy]):
        self.strategies = strategies

    def extract(self, file_path: str) -> dict:
        metadata = {}

        for strategy in self.strategies:
            result = strategy.extract(file_path)
            metadata.update(result)

        return metadata
