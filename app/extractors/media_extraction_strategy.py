from abc import ABC, abstractmethod


class MediaExtractionStrategy(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> dict:
        pass
