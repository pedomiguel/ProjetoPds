from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional

from jwt import encode, decode, DecodeError, ExpiredSignatureError, InvalidTokenError

from app.config import settings
from app.exceptions import UnauthorizedException


class AuthToken:

    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.expiration_in_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.algorithm = settings.ALGORITHM

    def generate_token(self, email: str):
        expire_at = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
            minutes=self.expiration_in_minutes
        )

        to_encode = {"exp": expire_at, "sub": email}

        encoded_jwt = encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt

    def decode_token(self, token: str) -> Optional[str]:
        try:
            payload = decode(token, self.secret_key, algorithms=self.algorithm)
            return payload.get("sub")
        except ExpiredSignatureError as exc:
            raise UnauthorizedException("Token has expired") from exc
        except InvalidTokenError as exc:
            raise UnauthorizedException("Invalid token") from exc
        except DecodeError:
            return None
