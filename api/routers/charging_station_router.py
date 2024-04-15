from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import UUID4
import logging
from ..crud import crud
from ..schemas import schemas
from ..database.database import get_db
from ..models.models import CurrentTypeEnum

logger = logging.getLogger(__name__)

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
    logger.info(f"Attempting to create a new charging station with data: {charging_station_data}")
    result = crud.create_charging_station(db=db, charging_station_data=charging_station_data)
    logger.info(f"Successfully created a charging station with ID: {result.id}")
    return result


@router.get(
    "/charging_stations/{charging_station_id}",
    response_model=schemas.ChargingStation,
    status_code=200,
    tags=["Charging Stations"],
    summary="Read a specific charging station providing its UUID"
)
def read_charging_station(charging_station_id: UUID4, db: Session = Depends(get_db)):
    logger.info(f"Fetching a charging station with ID: {charging_station_id}")
    result = crud.get_charging_station(db=db, charging_station_id=charging_station_id)
    logger.info(f"Successfully retrieved a charging station with ID: {charging_station_id}")
    return result


@router.get(
    "/charging_stations/",
    response_model=List[schemas.ChargingStation],
    status_code=200,
    tags=["Charging Stations"],
    summary="Read a list of all charging stations. Provide limit or skip values for pagination"
)
def read_charging_station_list(
        plug_count: int | None = None,
        min_efficiency: float | None = None,
        max_efficiency: float | None = None,
        current_type: CurrentTypeEnum | None = None,
        firmware_version: str | None = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    logger.info(
        f"Fetching a list of charging stations with filters: plug_count={plug_count}, min_efficiency={min_efficiency}, "
        f"max_efficiency={max_efficiency}, current_type={current_type}, firmware_version={firmware_version}, "
        f"skip={skip}, limit={limit}."
    )
    result = crud.get_charging_station_list(
        plug_count=plug_count,
        min_efficiency=min_efficiency,
        max_efficiency=max_efficiency,
        current_type=current_type,
        firmware_version=firmware_version,
        db=db,
        skip=skip,
        limit=limit
    )
    logger.info(f"Successfully retrieved {len(result)} charging stations.")
    return result


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
    logger.info(
        f"Attempting to update a charging station with ID: {charging_station_id} with data: "
        f"{charging_station_data}."
    )
    result = crud.update_charging_station(
        db=db,
        charging_station_id=charging_station_id,
        charging_station_data=charging_station_data
    )
    logger.info(f"Successfully updated a charging station with ID: {charging_station_id}.")
    return result


@router.delete(
    "/charging_stations/{charging_station_id}",
    status_code=204,
    tags=["Charging Stations"],
    summary="Delete a specific charging station providing its UUID"
)
def delete_charging_station(charging_station_id: UUID4, db: Session = Depends(get_db)):
    logger.info(f"Trying to delete a charging station with ID: {charging_station_id}.")
    result = crud.delete_charging_station(db=db, charging_station_id=charging_station_id)
    logger.info(f"Successfully deleted a charging station with ID: {charging_station_id}.")
    return result
