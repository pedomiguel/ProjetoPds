from fastapi.responses import JSONResponse

from app.repositories.user_repository import UserRepository
from app.schemas import AuthCreate, AuthLogin, AuthLoginResponse, UserCreate
from app.exceptions import (
    ConflictException,
    InvalidCredentialsException,
    NotFoundException,
)
from app.helpers import PasswordHash, AuthToken


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, user_create: AuthCreate):
        if self.user_repository.find_by_email(user_create.email):
            raise ConflictException("User already exists")

        password_hasher = PasswordHash()
        hashed_password = password_hasher.hash(user_create.password)

        user = UserCreate(
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password,
        )

        self.user_repository.create(user)

        return JSONResponse(content={"message": "User registered as successfully"})

    def login(self, login_data: AuthLogin) -> AuthLoginResponse:
        user = self.user_repository.find_by_email(login_data.email)

        if not user:
            raise NotFoundException("User not found")

        password_hasher = PasswordHash()

        if not password_hasher.verify(login_data.password, user.hashed_password):
            raise InvalidCredentialsException()

        token = AuthToken().generate_token(user.email)

        return AuthLoginResponse(access_token=token, token_type="Bearer", user=user)
