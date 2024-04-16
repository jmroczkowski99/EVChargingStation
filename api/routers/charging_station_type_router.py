from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import UUID4
import logging
from ..crud import crud
from ..schemas import schemas
from ..database.database import get_db
from ..models.models import CurrentTypeEnum
from ..utils.auth import get_current_user

logger = logging.getLogger(__name__)

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
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Attempting to create a charging station type with data: {charging_station_type_data}.")
    if not current_user:
        logger.error("Unauthorized attempt to create a charging station type.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to create a charging station type.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = crud.create_charging_station_type(db=db, charging_station_type_data=charging_station_type_data)
    logger.info(f"Successfully created a charging station type with ID: {result.id}.")
    return result


@router.get(
    "/charging_station_types/{charging_station_type_id}",
    response_model=schemas.ChargingStationType,
    status_code=200,
    tags=["Charging Station Types"],
    summary="Read a specific charging station type providing its UUID"
)
def read_charging_station_type(
        charging_station_type_id: UUID4,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Fetching a charging station type with ID: {charging_station_type_id}.")
    if not current_user:
        logger.error("Unauthorized attempt to retrieve a charging station type.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to retrieve a charging station type.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = crud.get_charging_station_type(db=db, charging_station_type_id=charging_station_type_id)
    logger.info(f"Successfully retrieved a charging station type with ID: {charging_station_type_id}.")
    return result


@router.get(
    "/charging_station_types/",
    response_model=List[schemas.ChargingStationType],
    status_code=200,
    tags=["Charging Station Types"],
    summary="Read a list of all charging station types. Provide limit or skip values for pagination"
)
def read_charging_station_type_list(
        plug_count: int | None = None,
        min_efficiency: float | None = None,
        max_efficiency: float | None = None,
        current_type: CurrentTypeEnum | None = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    logger.info(
        f"Fetching a list of charging station types with filters: plug_count={plug_count}, "
        f"min_efficiency={min_efficiency}, max_efficiency={max_efficiency}, current_type={current_type}, "
        f"skip={skip}, limit={limit}."
    )
    if not current_user:
        logger.error("Unauthorized attempt to retrieve charging station types.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to retrieve charging station types.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = crud.get_charging_station_type_list(
        plug_count=plug_count,
        min_efficiency=min_efficiency,
        max_efficiency=max_efficiency,
        current_type=current_type,
        skip=skip,
        limit=limit,
        db=db
    )
    logger.info(f"Successfully retrieved {len(result)} charging station types.")
    return result


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
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    logger.info(
        f"Attempting to update a charging station type with ID: {charging_station_type_id} "
        f"with data: {charging_station_type_data}."
    )
    if not current_user:
        logger.error("Unauthorized attempt to update a charging station type.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to update a charging station type.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = crud.update_charging_station_type(
        db=db,
        charging_station_type_id=charging_station_type_id,
        charging_station_type_data=charging_station_type_data
    )
    logger.info(f"Successfully updated a charging station type with ID: {charging_station_type_id}.")
    return result


@router.delete(
    "/charging_station_types/{charging_station_type_id}",
    status_code=204,
    tags=["Charging Station Types"],
    summary="Delete a specific charging station type providing its UUID"
)
def delete_charging_station_type(
        charging_station_type_id: UUID4,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Attempting to delete a charging station type with ID: {charging_station_type_id}.")
    if not current_user:
        logger.error("Unauthorized attempt to delete a charging station type.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to delete a charging station type.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = crud.delete_charging_station_type(db=db, charging_station_type_id=charging_station_type_id)
    logger.info(f"Successfully deleted a charging station type with ID: {charging_station_type_id}.")
    return result
