from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import UUID4
from ..crud import crud
from ..schemas import schemas
from ..database.database import get_db

router = APIRouter()


@router.post(
    "/charging_stations/",
    response_model=schemas.ChargingStation,
    status_code=201,
    tags=["Charging Stations"],
    summary="Create a new charging station"
)
def create_charging_station(
        charging_station_data: schemas.ChargingStationCreate,
        db: Session = Depends(get_db)
):
    return crud.create_charging_station(db=db, charging_station_data=charging_station_data)


@router.get(
    "/charging_stations/{charging_station_id}",
    response_model=schemas.ChargingStation,
    status_code=200,
    tags=["Charging Stations"],
    summary="Read a specific charging station providing its UUID"
)
def read_charging_station(charging_station_id: UUID4, db: Session = Depends(get_db)):
    return crud.get_charging_station(db=db, charging_station_id=charging_station_id)


@router.get(
    "/charging_stations/",
    response_model=List[schemas.ChargingStation],
    status_code=200,
    tags=["Charging Stations"],
    summary="Read a list of all charging stations. Provide limit or skip values for pagination"
)
def read_charging_station_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_charging_station_list(db=db, skip=skip, limit=limit)


@router.put(
    "/charging_stations/{charging_station_id}",
    response_model=schemas.ChargingStation,
    status_code=200,
    tags=["Charging Stations"],
    summary="Update a specific charging station providing its UUID"
)
def update_charging_station(
        charging_station_id: UUID4,
        charging_station_data: schemas.ChargingStationCreate,
        db: Session = Depends(get_db)
):
    return crud.update_charging_station(
        db=db,
        charging_station_id=charging_station_id,
        charging_station_data=charging_station_data
    )


@router.delete(
    "/charging_stations/{charging_station_id}",
    status_code=204,
    tags=["Charging Stations"],
    summary="Delete a specific charging station providing its UUID"
)
def delete_charging_station(charging_station_id: UUID4, db: Session = Depends(get_db)):
    return crud.delete_charging_station(db=db, charging_station_id=charging_station_id)
