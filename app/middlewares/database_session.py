
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.infrastructure.database.session_manager import DatabaseSessionManager

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db_session_manager = DatabaseSessionManager()
        session = db_session_manager.get_session()

        try:
            response = await call_next(request)
            session.commit()
            return response
        except Exception as e:
            session.rollback()
            raise e
        finally:
            db_session_manager.remove_session()