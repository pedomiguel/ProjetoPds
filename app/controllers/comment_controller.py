from uuid import UUID

from fastapi import Depends

from app.dependencies import AuthGuard
from app.models import User
from app.schemas import CommentResponse, CommentUpdate
from app.services.comment_service import CommentService

from .controller import BaseController


class CommentController(BaseController):
    def __init__(self):
        super().__init__(tags=["Comment"], prefix="/comment")
        self.comment_service = CommentService()

    def add_routes(self) -> None:
        @self.router.put("/{id}", response_model=CommentResponse)
        def update(
            id: UUID,
            data: CommentUpdate,
            user: User = Depends(AuthGuard.get_authenticated_user),
        ):
            comment_updated = self.comment_service.update(data, id, user)
            return CommentResponse.model_validate(comment_updated)

        @self.router.delete("/{id}")
        def delete(id: UUID, user: User = Depends(AuthGuard.get_authenticated_user)):
            commented_deleted = self.comment_service.delete(id, user)
            return CommentResponse.model_validate(commented_deleted)
