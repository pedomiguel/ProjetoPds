from abc import ABC, abstractmethod
from uuid import UUID

from app.models import MediaFile


class PipelineStepService(ABC):
    @abstractmethod
    def process(self, media: MediaFile, user_id: UUID) -> MediaFile:
        pass
