from typing import Optional

from fastapi import Header

from app.helpers import AuthToken
from app.repositories.user_repository import UserRepository
from app.models.user_model import User
from app.exceptions import UnauthorizedException, NotFoundException


class AuthGuard:
    @staticmethod
    async def get_authenticated_user(
        authorization: Optional[str] = Header(None),
    ) -> User:
        if not authorization:
            raise UnauthorizedException()

        _, token = authorization.split(" ")

        email = AuthToken().decode_token(token)

        if not email:
            raise UnauthorizedException()

        user_repo = UserRepository()
        user = user_repo.find_by_email(email)

        if not user:
            raise NotFoundException("User not found")

        return user
