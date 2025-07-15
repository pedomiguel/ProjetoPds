from uuid import UUID

from app.repositories import CommentRepository
from app.models import Comment
from app.schemas import CommentUpdate
from app.exceptions import ForbiddenException, NotFoundException
from app.models import User


class CommentService:
    def __init__(self) -> None:
        self.comment_repository = CommentRepository()

    def find_comment_by_id(self, id: int) -> Comment:
        comment = self.comment_repository.find_by_id(id)

        if not comment:
            raise NotFoundException("Comment not found")

        return comment

    def update(self, data: CommentUpdate, id: UUID, user: User) -> Comment:
        comment = self.find_comment_by_id(id)

        if comment.author_id != user.id:
            raise ForbiddenException("Unauthorized to update this comment")

        comment_updated = self.comment_repository.update(data, comment)

        return comment_updated

    def delete(self, id: UUID, user: User) -> Comment:
        comment = self.find_comment_by_id(id)

        if comment.author_id != user.id:
            raise ForbiddenException("Unauthorized to delete this comment")

        comment_deleted = self.comment_repository.delete(comment)

        return comment_deleted
