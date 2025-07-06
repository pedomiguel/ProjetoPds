from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse

from app.repositories import UserRepository, MediaFileRepository
from app.models import User
from app.schemas.user_schema import UserUpdate
from app.exceptions import NotFoundException, ConflictException


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.media_file_repository = MediaFileRepository()

    def user_profile(self, user: User) -> User:
        user = self.user_repository.find_by_id(user.id)

        if not user:
            raise NotFoundException("User not found")

        audios = self.media_file_repository.find_media_by_user_id(user.id)

        if audios:
            user.audios = audios

        return user

    def get_user_by_id(self, id: UUID) -> User:
        user = self.user_repository.find_by_id(id)

        if not user:
            raise NotFoundException(f"User not found")

        return user

    def update(self, data: UserUpdate, id: UUID) -> User:
        user = self.get_user_by_id(id)

        user_updated = self.user_repository.update(data, user)

        return user_updated

    def delete(self, id: UUID) -> User:
        user = self.get_user_by_id(id)

        user_deleted = self.user_repository.delete(user)

        return user_deleted

    def follow_user(self, follower: User, following_id: UUID) -> JSONResponse:
        if follower.id == following_id:
            raise ConflictException("You can't follow yourself")

        following_user = self.user_repository.find_by_id(following_id)

        if not following_user:
            raise NotFoundException("User not found")

        follower = self.user_repository.find_by_id(follower.id)

        if following_user in follower.following:
            raise ConflictException("You are already following this user")

        self.user_repository.add_follower(follower.id, following_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"You are following {following_user.name}"},
        )

    def unfollow_user(self, follower: User, following_id: UUID) -> JSONResponse:
        if follower.id == following_id:
            raise ConflictException("You can't unfollow yourself")

        following_user = self.user_repository.find_by_id(following_id)

        if not following_user:
            raise NotFoundException("User not found")

        follower = self.user_repository.find_by_id(follower.id)

        if following_user not in follower.following:
            raise ConflictException("You are not following this user")

        self.user_repository.remove_follower(follower.id, following_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"You have unfollowed {following_user.name}"},
        )
