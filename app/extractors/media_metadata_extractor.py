from abc import ABC, abstractmethod
from pathlib import Path


class MediaMetadataExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: Path) -> dict:
        pass
