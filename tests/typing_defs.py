from typing import Literal, TypedDict


# Add more literals in the future when more fields are added to the BROKEN_DB_DATA dictionary in conftest.py
BrokenDBDataTypeKey = Literal["MISSING_FIELD"]


class DriverType(TypedDict, total=False):
    driver_name: str
    driver_version: str
    driver_path: str
    driver_type: str


class MachineType(TypedDict, total=False):
    machine_id: str
    driver_id: int
    machine_model: str
    machine_manufacturer: str


class WorkingDBDataType(TypedDict):
    drivers: list[DriverType]
    machines: list[MachineType]


class BrokenDBCategoryType(TypedDict):
    drivers: list[DriverType]
    machines: list[MachineType]


class BrokenDBDataType(TypedDict):
    MISSING_FIELD: BrokenDBCategoryType
