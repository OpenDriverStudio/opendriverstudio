import tempfile
from pathlib import Path

import pytest

from src.opendriverstudio.database.database import Database, DatabaseCreationError
from tests.data_for_tests import WRONG_SYNTAX_SCHEMA


TESTING_DB_FILE = Path(__file__).parent / "tests.db"


@pytest.fixture
def empty_db_schema_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()  # Closing immediately to avoide locked file issues

    temp_file_path = Path(temp_file.name)

    yield temp_file_path

    if temp_file_path.exists():
        temp_file_path.unlink()


@pytest.fixture
def create_working_database():
    database_file = TESTING_DB_FILE

    db = Database(db_file=TESTING_DB_FILE)

    yield db

    if database_file.exists():
        database_file.unlink()


@pytest.fixture
def wrong_syntax_schema_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(WRONG_SYNTAX_SCHEMA)
    temp_file.close()

    temp_file_path = Path(temp_file.name)

    yield temp_file_path

    if temp_file_path.exists():
        temp_file_path.unlink()


class TestDatabase:
    def test_database_schema_is_empty(self, empty_db_schema_file) -> None:
        with pytest.raises(DatabaseCreationError):
            Database(db_file=TESTING_DB_FILE, db_schema=empty_db_schema_file)

    def test_database_is_created_successfully(self, create_working_database) -> None:
        db: Database = create_working_database

        assert Path.exists(db.db_file)
        assert Path(db.db_file).stat().st_size > 0

    def test_database_schema_has_wrong_syntax(self, wrong_syntax_schema_file) -> None:
        with pytest.raises(DatabaseCreationError):
            Database(db_file=TESTING_DB_FILE, db_schema=wrong_syntax_schema_file)
