from app.models import Comment
from app.schemas import CommentCreate

from .repository import Repository


class CommentRepository(Repository[Comment, CommentCreate, None]):
    @property
    def model(self) -> type[Comment]:
        return Comment
