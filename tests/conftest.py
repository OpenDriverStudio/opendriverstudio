import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from src.opendriverstudio.database.database import Database
from tests.typing_defs import BrokenDBDataType, BrokenDBDataTypeKey, DriverType, MachineType, WorkingDBDataType


TESTING_DB_FILE = Path(__file__).parent / "tests.db"

WRONG_SYNTAX_SCHEMA = b"CREATE TABLE test (id INTEGER"  # Wrong syntax on purpose

WORKING_DB_DATA: WorkingDBDataType = {
    "drivers": [
        {
            "driver_name": "sp142670",
            "driver_version": "3.00 REV: A PASS: 1",
            "driver_path": "/path/to/driver",
            "driver_type": "driverpack",
        },
        {
            "driver_name": "sp154299",
            "driver_version": "7.00 REV: A PASS: 1",
            "driver_path": "/path/to/driver/2",
            "driver_type": "driverpack",
        },
    ],
    "machines": [
        {
            "machine_id": "8848",
            "driver_id": 1,
            "machine_model": "HP EliteBook 850 G8 Notebook PC",
            "machine_manufacturer": "HP",
        },
        {
            "machine_id": "894F",
            "driver_id": 2,
            "machine_model": "HP Elite Mini 800 G9 Desktop PC",
            "machine_manufacturer": "HP",
        },
    ],
}

BROKEN_DB_DATA: BrokenDBDataType = {
    "MISSING_FIELD": {
        "drivers": [
            {
                # "driver_name": "sp142670",  # Missing parameter
                "driver_version": "3.00 REV: A PASS: 1",
                "driver_path": "/path/to/driver",
                "driver_type": "driverpack",
            },
            {
                "driver_name": "sp142670",
                # "driver_version": "33.00 REV: A PASS: 1",  # Missing parameter
                "driver_path": "/path/to/driver",
                "driver_type": "driverpack",
            },
            {
                "driver_name": "sp142670",
                "driver_version": "3.00 REV: A PASS: 1",
                # "driver_path": "/path/to/driver",  # Missing parameter
                "driver_type": "driverpack",
            },
            {
                "driver_name": "sp142670",
                "driver_version": "3.00 REV: A PASS: 1",
                "driver_path": "/path/to/driver",
                # "driver_type": "driverpack",  # Missing parameter
            },
        ],
        "machines": [
            {
                # "machine_id": "8848",  # Missing parameter
                "driver_id": 1,
                "machine_model": "HP EliteBook 850 G8 Notebook PC",
                "machine_manufacturer": "HP",
            },
            {
                "machine_id": "8848",
                # "driver_id": 1,  # Missing parameter
                "machine_model": "HP EliteBook 850 G8 Notebook PC",
                "machine_manufacturer": "HP",
            },
            {
                "machine_id": "8848",
                "driver_id": 1,
                # "machine_model": "HP EliteBook 850 G8 Notebook PC",  # Missing parameter
                "machine_manufacturer": "HP",
            },
            {
                "machine_id": "8848",
                "driver_id": 1,
                "machine_model": "HP EliteBook 850 G8 Notebook PC",
                # "machine_manufacturer": "HP",  # Missing parameter
            },
        ],
    },
}


@pytest.fixture
def working_drivers_db_data() -> list[DriverType]:
    return WORKING_DB_DATA["drivers"]


@pytest.fixture
def working_machines_db_data() -> list[MachineType]:
    return WORKING_DB_DATA["machines"]


@pytest.fixture(params=["MISSING_FIELD"])
def broken_drivers_db_data(request: pytest.FixtureRequest) -> list[DriverType]:
    # This param variable is created like this so that mypy doesn't complain.
    # If you do `return BROKEN_DB_DATA[request.param]...` mypy complains that it expected a literal string.
    param: BrokenDBDataTypeKey = request.param
    return BROKEN_DB_DATA[param]["drivers"]


@pytest.fixture(params=["MISSING_FIELD"])
def broken_machines_db_data(request: pytest.FixtureRequest) -> list[MachineType]:
    # This param variable is created like this so that mypy doesn't complain.
    # If you do `return BROKEN_DB_DATA[request.param]...` mypy complains that it expected a literal string.
    param: BrokenDBDataTypeKey = request.param
    return BROKEN_DB_DATA[param]["machines"]


@pytest.fixture
def empty_db_schema_file() -> Generator[Path, None, None]:
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # noqa: SIM115
    temp_file.close()  # Closing immediately to avoide locked file issues

    temp_file_path = Path(temp_file.name)

    yield temp_file_path

    if temp_file_path.exists():
        temp_file_path.unlink()


@pytest.fixture
def create_working_database() -> Generator[Database, None, None]:
    database_file = TESTING_DB_FILE

    db = Database(db_file=TESTING_DB_FILE)

    yield db

    if database_file.exists():
        database_file.unlink()


@pytest.fixture
def wrong_syntax_schema_file() -> Generator[Path, None, None]:
    temp_file = tempfile.NamedTemporaryFile(delete=False)  # noqa: SIM115
    temp_file.write(WRONG_SYNTAX_SCHEMA)
    temp_file.close()

    temp_file_path = Path(temp_file.name)

    yield temp_file_path

    if temp_file_path.exists():
        temp_file_path.unlink()


@pytest.fixture
def testing_drivers_db_data() -> list[tuple[int, str, str, str, str]]:
    return [
        (
            id + 1,  # Generate driver_id starting from 1
            driver["driver_name"],
            driver["driver_version"],
            driver["driver_path"],
            driver["driver_type"],
        )
        for id, driver in enumerate(WORKING_DB_DATA["drivers"])
    ]


@pytest.fixture
def testing_api_driver_db_data() -> list[list[int | str]]:
    return [
        [
            id + 1,  # Generate driver_id starting from 1
            driver["driver_name"],
            driver["driver_version"],
            driver["driver_path"],
            driver["driver_type"],
        ]
        for id, driver in enumerate(WORKING_DB_DATA["drivers"])
    ]


@pytest.fixture
def setup_database_with_working_drivers_data(
    create_working_database,
    working_drivers_db_data,
) -> Generator[Database, None, None]:
    db: Database = create_working_database

    for driver in working_drivers_db_data:
        db.insert_into_drivers_table(driver)

    yield db  # noqa: PT022
