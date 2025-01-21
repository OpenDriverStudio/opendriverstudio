from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.opendriverstudio.database.database import DatabaseInsertionError, DriverDatabase
from src.opendriverstudio.database.schema import Driver


router = APIRouter()


def get_database() -> DriverDatabase:
    return DriverDatabase()


@router.get("/drivers")
async def get_all_drivers(db: Annotated[DriverDatabase, Depends(get_database)]) -> list[tuple[int, str, str, str, str]]:
    return db.select_all_from_drivers_table()


@router.get("/drivers/name={driver_name}")
async def get_driver_id_from_driver_name(
    db: Annotated[DriverDatabase, Depends(get_database)],
    driver_name: str,
) -> dict[str, int | None]:
    driver_id = db.select_driver_id_from_drivers_with_driver_name(driver_name)

    return {"driver_id": driver_id}


@router.post("/drivers", responses={409: {"description": "Conflict: Database insertion error."}})
async def add_driver(
    db: Annotated[DriverDatabase, Depends(get_database)],
    driver: Driver,
) -> dict[str, str]:
    rows = driver.model_dump()

    try:
        db.insert_into_drivers_table(rows)
        return {"status": "Driver added successfully"}
    except DatabaseInsertionError as e:
        raise HTTPException(status_code=409, detail=f"{e}") from e
