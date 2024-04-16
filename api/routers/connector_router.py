from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import UUID4
import logging
from ..crud import crud
from ..schemas import schemas
from ..database.database import get_db
from ..utils.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/connectors/",
    response_model=schemas.Connector,
    status_code=201,
    tags=["Connectors"],
    summary="Create a new connector"
)
def create_connector(
        connector_data: schemas.ConnectorCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Attempting to create a connector with data: {connector_data}.")
    if not current_user:
        logger.error("Unauthorized attempt to create a connector.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to create a connector.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = crud.create_connector(db=db, connector_data=connector_data)
    logger.info(f"Successfully created a connector with ID: {result.id}.")
    return result


@router.get(
    "/connectors/{connector_id}",
    response_model=schemas.Connector,
    status_code=200,
    tags=["Connectors"],
    summary="Read a specific connector providing its UUID"
)
def read_connector(
        connector_id: UUID4,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Fetching a connector with ID: {connector_id}.")
    if not current_user:
        logger.error("Unauthorized attempt to retrieve a connector.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to retrieve a connector.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = crud.get_connector(db=db, connector_id=connector_id)
    logger.info(f"Successfully retrieved a connector with ID: {connector_id}.")
    return result


@router.get(
    "/connectors/",
    response_model=List[schemas.Connector],
    status_code=200,
    tags=["Connectors"],
    summary="Read a list of all connectors. Provide limit or skip values for pagination"
)
def read_connector_list(
        priority: bool | None = None,
        charging_station_id: UUID4 | None = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user),
):
    logger.info(
        f"Fetching a list of connectors with filters: priority={priority}, charging_station_id={charging_station_id}, "
        f"skip={skip}, limit={limit}."
    )
    if not current_user:
        logger.error("Unauthorized attempt to retrieve connectors.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to retrieve connectors.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = crud.get_connector_list(
        priority=priority,
        charging_station_id=charging_station_id,
        skip=skip,
        limit=limit,
        db=db,
    )
    logger.info(f"Successfully retrieved {len(result)} connectors.")
    return result


@router.put(
    "/connectors/{connector_id}",
    response_model=schemas.Connector,
    status_code=200,
    tags=["Connectors"],
    summary="Update a specific connector providing its UUID"
)
def update_connector(
        connector_id: UUID4,
        connector_data: schemas.ConnectorCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user),
):
    logger.info(f"Attempting to update a connector with ID: {connector_id} with data: {connector_data}.")
    if not current_user:
        logger.error("Unauthorized attempt to update a connector.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to update a connector.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = crud.update_connector(
        db=db,
        connector_id=connector_id,
        connector_data=connector_data
    )
    logger.info(f"Succesfully updated a connector with ID: {connector_id}.")
    return result


@router.delete(
    "/connectors/{connector_id}",
    status_code=204,
    tags=["Connectors"],
    summary="Delete a specific connector providing its UUID"
)
def delete_connector(
        connector_id: UUID4,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Attempting to delete a connector with ID: {connector_id}.")
    if not current_user:
        logger.error("Unauthorized attempt to delete a connector.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to delete a connector.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    result = crud.delete_connector(db=db, connector_id=connector_id)
    logger.info(f"Successfully deleted a connector with ID: {connector_id}.")
    return result
