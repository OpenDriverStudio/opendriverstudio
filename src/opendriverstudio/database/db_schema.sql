CREATE TABLE IF NOT EXISTS drivers (
    driver_id INTEGER PRIMARY KEY,
    driver_name TEXT NOT NULL UNIQUE,
    driver_version TEXT NOT NULL,
    driver_path TEXT NOT NULL,
    driver_type TEXT NOT NULL
) STRICT;

CREATE TABLE IF NOT EXISTS drivers_upkeep (
    driver_id INTEGER NOT NULL,
    download_datetime TEXT NOT NULL,  -- ISO8601 format ("YYYY-MM-DD HH:MM:SS.SSS") UTC time
    update_datetime TEXT NOT NULL, -- ISO8601 format ("YYYY-MM-DD HH:MM:SS.SSS") UTC time
    uri TEXT NOT NULL,
    FOREIGN KEY (driver_id)
        REFERENCES drivers (driver_id)
        ON DELETE CASCADE,
    CHECK (download_datetime GLOB '????-??-?? ??:??:??.???'),  -- Check for ISO8601 pattern
    CHECK (update_datetime GLOB '????-??-?? ??:??:??.???')  -- Check for ISO8601 pattern
) STRICT;

CREATE TABLE IF NOT EXISTS machines (
    machine_id TEXT NOT NULL,
    driver_id INTEGER NOT NULL,
    machine_model TEXT NOT NULL,
    machine_manufacturer TEXT NOT NULL,
    PRIMARY KEY (machine_id),
    FOREIGN KEY (driver_id)
        REFERENCES drivers (driver_id)
        ON DELETE CASCADE
) STRICT;
