from uuid import UUID

from fastapi.responses import JSONResponse
from fastapi import status

from app.repositories import PostRepository, MediaFileRepository, CommentRepository
from app.schemas import PostCreateRequest, PostCreate, PostUpdate, CommentCreate
from app.exceptions import NotFoundException
from app.models import User, Post


class PostService:
    def __init__(self):
        self.post_repository = PostRepository()
        self.media_repository = MediaFileRepository()
        self.comment_repository = CommentRepository()

    def create_post(self, data: PostCreateRequest, user: User) -> JSONResponse:
        media_ids = data.media_ids
        medias = self.media_repository.find_by_ids(media_ids)
        medias_dict = {media.id: media for media in medias}

        missing_media_ids = []

        for media_id in media_ids:
            media = medias_dict.get(media_id)
            if not media or media.user_id != user.id:
                missing_media_ids.append(media_id)

        if missing_media_ids:
            missing_str = ", ".join(str(id) for id in missing_media_ids)
            raise NotFoundException(
                "Media files not found",
                errors=[f"Media files with IDs: {missing_str} not found"],
            )

        post = self.post_repository.create(
            PostCreate(**data.model_dump(), author_id=user.id)
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"id": str(post.id), "message": "Post created successfully"},
        )

    def get_post_by_id(self, post_id: UUID):
        post = self.post_repository.find_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found")

        return post

    def __set_author_following_flag(self, posts: list[Post], user: User):
        followed_ids = {u.id for u in user.following}

        for post in posts:
            post.author.is_following = post.author.id in followed_ids

        return posts

    def get_my_posts(self, user: User, theme: str | None = None):
        return self.post_repository.get_all(author_ids=[user.id], theme=theme)

    def get_feed_posts(self, user: User, theme: str | None = None):
        following_ids = [u.id for u in user.following]
        author_ids = [user.id] + following_ids

        posts = self.post_repository.get_all(theme=theme, author_ids=author_ids)
        return self.__set_author_following_flag(posts, user)

    def list_all_posts(self, user: User, theme: str | None = None):
        posts = self.post_repository.get_all(theme=theme)
        return self.__set_author_following_flag(posts, user)

    def delete_post(self, post_id: UUID) -> JSONResponse:
        post = self.post_repository.find_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found")

        self.post_repository.delete(post)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Post deleted successfully"},
        )

    def update_post(self, post_id: UUID, data: PostUpdate):
        post = self.post_repository.find_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found")

        updated_post = self.post_repository.update(data, post)
        return updated_post

    def add_comment(
        self, post_id: UUID, data: CommentCreate, user: User
    ) -> JSONResponse:
        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise NotFoundException("Post not found")

        self.comment_repository.create(
            CommentCreate(
                content=data.content,
                post_id=post_id,
                author_id=user.id,
            )
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Comment added successfully"},
        )
