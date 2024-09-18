import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent
DATABASE_FILE = DATABASE_PATH / "opendriverstudio.db"
DATABASE_SCHEMA = DATABASE_PATH / "db_schema.sql"


class Database:
    def __init__(self, db_file: Path = DATABASE_FILE, db_schema: Path = DATABASE_SCHEMA) -> None:
        self.db_file = db_file
        self.db_schema = db_schema

        if not self._does_db_exist():
            self._create_db()

    def _does_db_exist(self) -> bool:
        return Path.exists(self.db_file)

    def _create_db(self) -> None:
        if self.db_schema.stat().st_size == 0:
            raise DatabaseCreationError("Database schema file is empty")

        connection = sqlite3.connect(self.db_file)

        sql_script = self.db_schema.read_text()

        try:
            with connection:
                connection.executescript(sql_script)
        except sqlite3.OperationalError as e:
            connection.close()
            self.db_file.unlink()

            raise DatabaseCreationError("Error creating database.") from e
        else:
            connection.close()
        finally:
            del connection


class DatabaseCreationError(Exception):
    pass
