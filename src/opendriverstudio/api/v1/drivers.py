from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.opendriverstudio.database.database import Database, DatabaseInsertionError


router = APIRouter()


def get_database() -> Database:
    return Database()


@router.get("/drivers")
async def get_all_drivers(db: Annotated[Database, Depends(get_database)]) -> list[tuple[int, str, str, str, str]]:
    return db.select_all_from_drivers_table()


@router.get("/drivers/name={driver_name}")
async def get_driver_id_from_driver_name(
    db: Annotated[Database, Depends(get_database)],
    driver_name: str,
) -> dict[str, int | None]:
    driver_id = db.select_driver_id_from_drivers_with_driver_name(driver_name)

    return {"driver_id": driver_id}


@router.post("/drivers", responses={409: {"description": "Conflict: Database insertion error."}})
async def add_driver(
    db: Annotated[Database, Depends(get_database)],
    driver_name: str,
    driver_version: str,
    driver_path: str,
    driver_type: str,
) -> dict[str, str]:
    rows = {
        "driver_name": driver_name,
        "driver_version": driver_version,
        "driver_path": driver_path,
        "driver_type": driver_type,
    }

    try:
        db.insert_into_drivers_table(rows)
        return {"status": "Driver added successfully"}
    except DatabaseInsertionError as e:
        raise HTTPException(status_code=409, detail=f"{e}") from e
