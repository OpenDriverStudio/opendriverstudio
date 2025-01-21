import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any


DATABASE_PATH = Path(__file__).parent
DATABASE_FILE = DATABASE_PATH / "opendriverstudio.db"
DATABASE_SCHEMA = DATABASE_PATH / "db_schema.sql"


class BaseDatabase:
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

    @contextmanager
    def _get_db_connection(self) -> Generator[sqlite3.Connection, None, None]:
        connection = sqlite3.connect(self.db_file)
        try:
            yield connection
        finally:
            connection.close()


class DriverDatabase(BaseDatabase):
    def insert_into_drivers_table(self, data: dict[str, Any]) -> None:
        sql_query = """
            INSERT INTO drivers (driver_name, driver_version, driver_path, driver_type)
            VALUES (?, ?, ?, ?)
            """

        try:
            sql_parameters = (data["driver_name"], data["driver_version"], data["driver_path"], data["driver_type"])
        except KeyError as e:
            raise MissingFieldError(f"Missing field {e} from insert data.") from None

        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql_query, sql_parameters)
                conn.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
            raise DatabaseInsertionError(f"Error inserting data into table 'drivers': {e}") from e

    def select_all_from_drivers_table(self) -> list[tuple[int, str, str, str, str]]:
        sql_query = "SELECT * FROM drivers"

        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            return cursor.fetchall()

    def select_driver_id_from_drivers_with_driver_name(self, driver_name: str) -> int | None:
        sql_query = "SELECT driver_id FROM drivers WHERE driver_name = ?"

        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query, (driver_name,))
            result = cursor.fetchone()
            return result[0] if result else None


class DatabaseCreationError(Exception):
    pass


class DatabaseInsertionError(Exception):
    pass


class MissingFieldError(DatabaseInsertionError):
    pass
