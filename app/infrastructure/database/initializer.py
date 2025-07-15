from app.config import BaseModel
from .session_manager import DatabaseSessionManager
from .creator import DatabaseCreator


class DatabaseInitializer:

    @staticmethod
    def run():
        DatabaseCreator().create_database_if_not_exists()

        database_engine = DatabaseSessionManager().get_engine()

        BaseModel.metadata.create_all(bind=database_engine)
