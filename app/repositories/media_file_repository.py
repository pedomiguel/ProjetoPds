from uuid import UUID
from sqlalchemy.orm import joinedload

from app.models.media_file_model import MediaFile
from app.schemas.media_file_schema import MediaFileCreate, MediaFileUpdate

from .repository import Repository


class MediaFileRepository(Repository[MediaFile, MediaFileCreate, MediaFileUpdate]):
    @property
    def model(self) -> type[MediaFile]:
        return MediaFile

    def find_media_by_user_id(
        self, user_id: UUID, limit: int | None = None
    ) -> list[MediaFile]:
        query = (
            self.db.query(MediaFile)
            .filter(MediaFile.user_id == user_id, MediaFile.parent_id == None)
            .options(
                joinedload(MediaFile.children),
            )
            .order_by(MediaFile.date_in.desc())
        )

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def is_parent(self, id: UUID) -> bool:
        media = self.find_by_id(id)
        return media.parent_id is None
