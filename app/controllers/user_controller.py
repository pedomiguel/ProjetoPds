from fastapi import Depends

from app.dependencies import AuthGuard
from app.models import User
from app.schemas import UserResponse, UserResponseWithMediaFiles
from app.schemas.user_schema import UserUpdate, FollowUserRequest
from app.services import UserService

from .controller import BaseController


class UserController(BaseController):
    def __init__(self):
        super().__init__(tags=["User"], prefix="/user")
        self.user_service = UserService()

    def add_routes(self) -> None:
        @self.router.get("/me", response_model=UserResponseWithMediaFiles)
        def me(user: User = Depends(AuthGuard.get_authenticated_user)):
            user = self.user_service.user_profile(user)

            return UserResponseWithMediaFiles.model_validate(user)

        @self.router.post("/follow")
        def follow_user(
            body: FollowUserRequest,
            user: User = Depends(AuthGuard.get_authenticated_user),
        ):
            return self.user_service.follow_user(user, body.user_id)

        @self.router.delete("/unfollow")
        def unfollow_user(
            body: FollowUserRequest,
            user: User = Depends(AuthGuard.get_authenticated_user),
        ):
            return self.user_service.unfollow_user(user, body.user_id)

        @self.router.put("/update")
        def update(
            data: UserUpdate, user: User = Depends(AuthGuard.get_authenticated_user)
        ):
            user_updated = self.user_service.update(data, user.id)
            return UserResponse.model_validate(user_updated)

        @self.router.delete("/delete")
        def delete(user: User = Depends(AuthGuard.get_authenticated_user)):
            user_deleted = self.user_service.delete(user.id)
            return UserResponse.model_validate(user_deleted)
