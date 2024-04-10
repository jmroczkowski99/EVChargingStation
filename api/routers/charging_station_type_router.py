from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import UUID4
from ..crud import crud
from ..schemas import schemas
from ..database.database import get_db

router = APIRouter()


@router.post(
    "/charging_station_types/",
    response_model=schemas.ChargingStationType,
    status_code=201,
    tags=["Charging Station Types"],
    summary="Create a new charging station type"
)
def create_charging_station_type(
        charging_station_type_data: schemas.ChargingStationTypeCreate,
        db: Session = Depends(get_db)
):
    return crud.create_charging_station_type(db=db, charging_station_type_data=charging_station_type_data)


@router.get(
    "/charging_station_types/{charging_station_type_id}",
    response_model=schemas.ChargingStationType,
    status_code=200,
    tags=["Charging Station Types"],
    summary="Read a specific charging station type providing its UUID"
)
def read_charging_station_type(charging_station_type_id: UUID4, db: Session = Depends(get_db)):
    return crud.get_charging_station_type(db=db, charging_station_type_id=charging_station_type_id)


@router.get(
    "/charging_station_types/",
    response_model=List[schemas.ChargingStationType],
    status_code=200,
    tags=["Charging Station Types"],
    summary="Read a list of all charging station types. Provide limit or skip values for pagination"
)
def read_charging_station_type_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_charging_station_type_list(db=db, skip=skip, limit=limit)


@router.put(
    "/charging_station_types/{charging_station_type_id}",
    response_model=schemas.ChargingStationType,
    status_code=200,
    tags=["Charging Station Types"],
    summary="Update a specific charging station type providing its UUID"
)
def update_charging_station_type(
        charging_station_type_id: UUID4,
        charging_station_type_data: schemas.ChargingStationTypeCreate,
        db: Session = Depends(get_db)
):
    return crud.update_charging_station_type(
        db=db,
        charging_station_type_id=charging_station_type_id,
        charging_station_type_data=charging_station_type_data
    )


@router.delete(
    "/charging_station_types/{charging_station_type_id}",
    status_code=204,
    tags=["Charging Station Types"],
    summary="Delete a specific charging station type providing its UUID"
)
def delete_charging_station_type(charging_station_type_id: UUID4, db: Session = Depends(get_db)):
    return crud.delete_charging_station_type(db=db, charging_station_type_id=charging_station_type_id)
