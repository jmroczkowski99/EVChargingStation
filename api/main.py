from fastapi import FastAPI
from .database.database import init_db
from .routers import charging_station_type_router, charging_station_router, connector_router
from .utils.logging_config import setup_logging

setup_logging()

app = FastAPI(
    title="EVChargingStation",
    description="This API allows you to manage EV charging stations, their types and connectors."
)


@app.on_event("startup")
def startup_event():
    init_db()


app.include_router(charging_station_type_router.router, tags=["Charging Station Types"])
app.include_router(charging_station_router.router, tags=["Charging Stations"])
app.include_router(connector_router.router, tags=["Connectors"])
