from pydantic import BaseModel, EmailStr
from app.schemas import UserBase


class AuthCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class AuthLogin(BaseModel):
    email: EmailStr
    password: str


class AuthLoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserBase
