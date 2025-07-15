from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config.settings import settings
from app.infrastructure.singleton_meta import SingletonMeta


class DatabaseSessionManager(metaclass=SingletonMeta):
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL, echo=True)
        self.session_factory = sessionmaker(bind=self.engine)
        self.scoped_session = scoped_session(self.session_factory)

    def get_session(self):
        return self.scoped_session()

    def remove_session(self):
        self.scoped_session.remove()

    def get_engine(self):
        return self.engine
