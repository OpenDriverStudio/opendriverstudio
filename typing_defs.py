from typing import TypedDict


class DriverType(TypedDict):
    driver_name: str
    driver_version: str
    driver_path: str
    driver_type: str


class MachineType(TypedDict):
    machine_id: str
    driver_id: int
    machine_model: str
    machine_manufacturer: str


class WorkingDBDataType(TypedDict):
    drivers: list[DriverType]
    machines: list[MachineType]
