from pathlib import Path

import pytest

from src.opendriverstudio.database.database import Database, DatabaseCreationError, MissingFieldError
from tests.conftest import TESTING_DB_FILE


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

    def test_database_insert_into_drivers_table(self, create_working_database, working_drivers_db_data) -> None:
        db: Database = create_working_database

        for driver in working_drivers_db_data:
            db.insert_into_drivers_table(driver)

    def test_database_insert_into_drivers_table_with_missing_field(
        self,
        create_working_database,
        broken_drivers_db_data,
    ) -> None:
        db: Database = create_working_database

        for driver in broken_drivers_db_data:
            with pytest.raises(MissingFieldError):
                db.insert_into_drivers_table(driver)

    def test_database_select_all_from_drivers_table(
        self,
        setup_database_with_working_drivers_data,
        testing_drivers_db_data,
    ) -> None:
        db: Database = setup_database_with_working_drivers_data

        db_output = db.select_all_from_drivers_table()

        assert db_output == testing_drivers_db_data

    def test_database_select_driver_id_from_drivers_with_driver_name(
        self,
        setup_database_with_working_drivers_data,
    ) -> None:
        db: Database = setup_database_with_working_drivers_data

        db_output_1 = db.select_driver_id_from_drivers_with_driver_name("sp142670")
        db_output_2 = db.select_driver_id_from_drivers_with_driver_name("sp154299")

        assert db_output_1 == 1
        assert db_output_2 == 2
