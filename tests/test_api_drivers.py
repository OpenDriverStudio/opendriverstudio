from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.opendriverstudio.api.v1 import drivers
from src.opendriverstudio.database.database import Database
from tests.conftest import TESTING_DB_FILE


def override_get_database() -> Generator[Database, None, None]:
    database_file = TESTING_DB_FILE

    db = Database(db_file=database_file)
    yield db

    if database_file.exists():
        database_file.unlink()


app = FastAPI()
app.include_router(drivers.router, tags=["Drivers"])
app.dependency_overrides[drivers.get_database] = override_get_database

client = TestClient(app)


def test_get_all_drivers(setup_database_with_working_drivers_data, testing_api_driver_db_data) -> None:
    response = client.get("/drivers")
    assert response.status_code == 200
    assert response.json() == list(testing_api_driver_db_data)


@pytest.mark.parametrize(
    ("driver_name", "expected_driver_id"),
    [
        ("sp142670", 1),
        ("sp154299", 2),
    ],
)
def test_get_driver_id_from_driver_name(setup_database_with_working_drivers_data, driver_name, expected_driver_id):
    response = client.get(f"/drivers/name={driver_name}")
    assert response.status_code == 200
    assert response.json() == {"driver_id": expected_driver_id}


def test_add_driver(setup_database_with_working_drivers_data):
    response = client.post(
        "/drivers",
        json={
            "driver_name": "Driver3",
            "driver_version": "v3.0",
            "driver_path": "/path/to/driver3",
            "driver_type": "bios",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"status": "Driver added successfully"}


def test_add_driver_conflict(setup_database_with_working_drivers_data):
    response = client.post(
        "/drivers",
        json={
            "driver_name": "sp142670",
            "driver_version": "v1.0",
            "driver_path": "/path/to/driver1",
            "driver_type": "type1",
        },
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Error inserting data into table 'drivers': UNIQUE constraint failed: drivers.driver_name",
    }
