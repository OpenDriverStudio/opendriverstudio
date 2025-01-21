from pydantic import BaseModel


class Driver(BaseModel):
    driver_id: int | None = None
    driver_name: str
    driver_version: str
    driver_path: str
    driver_type: str
