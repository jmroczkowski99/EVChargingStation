from fastapi import FastAPI
from .routers import charging_station_type_router, charging_station_router, connector_router

app = FastAPI(
    title="EVChargingStation",
    description="This API allows you to manage EV charging stations, their types and connectors."
)

app.include_router(charging_station_type_router.router, tags=["Charging Station Types"])
app.include_router(charging_station_router.router, tags=["Charging Stations"])
app.include_router(connector_router.router, tags=["Connectors"])
