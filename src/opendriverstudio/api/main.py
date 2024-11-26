from fastapi import FastAPI

from src.opendriverstudio.api.v1 import drivers


app = FastAPI()

app.include_router(drivers.router, prefix="/api/v1", tags=["Drivers"])
