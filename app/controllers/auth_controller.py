from fastapi import APIRouter

from app.services.auth_service import AuthService
from app.schemas.auth_schema import AuthCreate, AuthLogin, AuthLoginResponse

from .controller import BaseController


class AuthController(BaseController):
    def __init__(self):
        super().__init__(tags=["Auth"])
        self._auth_service = AuthService()

    @property
    def router(self) -> APIRouter:
        return self._router

    def add_routes(self) -> None:
        @self.router.post("/register")
        def register(user: AuthCreate):
            return self._auth_service.register(user)

        @self.router.post("/login", response_model=AuthLoginResponse)
        def login(user: AuthLogin):
            return self._auth_service.login(user)
