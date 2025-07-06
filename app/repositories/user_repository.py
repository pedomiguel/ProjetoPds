from uuid import UUID
from sqlalchemy.orm import joinedload, noload

from app.models import User, UserFollower
from app.schemas.user_schema import UserCreate, UserUpdate

from .repository import Repository


class UserRepository(Repository[User, UserCreate, UserUpdate]):
    @property
    def model(self) -> type[User]:
        return User

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def add_follower(self, follower_id: UUID, following_id: UUID) -> UserFollower:
        follow = UserFollower(follower_id=follower_id, following_id=following_id)
        self.db.add(follow)
        self.db.commit()

        return follow

    def remove_follower(self, follower_id: UUID, following_id: UUID) -> None:
        self.db.query(UserFollower).filter(
            UserFollower.follower_id == follower_id,
            UserFollower.following_id == following_id,
        ).delete()
        self.db.commit()

    def find_by_id(self, id: int | UUID) -> User:
        return (
            self.db.query(User)
            .options(noload(User.media_files))
            .options(joinedload(User.followers), joinedload(User.following))
            .filter(User.id == id)
            .first()
        )
