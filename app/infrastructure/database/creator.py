import psycopg2
from urllib.parse import urlparse
from app.config.logger import Logger
from app.config.settings import settings


class DatabaseCreator:
    def __init__(self):
        self.db_url = settings.DATABASE_URL
        self.db_name = self._extract_db_name()
        self.admin_url = self._build_admin_url()

    def _extract_db_name(self) -> str:
        return urlparse(self.db_url).path.lstrip("/")

    def _build_admin_url(self, admin_db: str = "postgres") -> str:
        parsed = urlparse(self.db_url)
        return f"{parsed.scheme}://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}/{admin_db}"

    def _run_query(self, query: str):
        try:
            conn = psycopg2.connect(self.admin_url)
            conn.set_session(autocommit=True)
            with conn.cursor() as cur:
                cur.execute(query)

                if query.strip().lower().startswith("select"):
                    return cur.fetchone()

                return True
        except Exception as e:
            Logger.error(
                __name__,
                f"Error executing query for the database '{self.db_name}': {e}",
            )
            return None
        finally:
            if "conn" in locals():
                conn.close()

    def database_exists(self) -> bool:
        try:
            result = self._run_query(
                f"SELECT 1 FROM pg_database WHERE datname = '{self.db_name}'"
            )
            return result is not None
        except Exception as e:
            Logger.error(
                __name__,
                f"Error checking existence of the database '{self.db_name}': {e}",
            )
            return False

    def create_database_if_not_exists(self):
        if not self.database_exists():
            query = f"CREATE DATABASE {self.db_name}"
            if self._run_query(query) is None:
                Logger.error(__name__, f"Failed to create database '{self.db_name}'")
            else:
                Logger.info(
                    __name__, f"Database '{self.db_name}' created successfully!"
                )
        else:
            Logger.info(__name__, f"The database '{self.db_name}' already exists!")
