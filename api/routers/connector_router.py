from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import UUID4
from ..crud import crud
from ..schemas import schemas
from ..database.database import get_db

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
        db: Session = Depends(get_db)
):
    return crud.create_connector(db=db, connector_data=connector_data)


@router.get(
    "/connectors/{connector_id}",
    response_model=schemas.Connector,
    status_code=200,
    tags=["Connectors"],
    summary="Read a specific connector providing its UUID"
)
def read_connector(connector_id: UUID4, db: Session = Depends(get_db)):
    return crud.get_connector(db=db, connector_id=connector_id)


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
        db: Session = Depends(get_db)
):
    return crud.get_connector_list(
        priority=priority,
        charging_station_id=charging_station_id,
        skip=skip,
        limit=limit,
        db=db,
    )


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
        db: Session = Depends(get_db)
):
    return crud.update_connector(
        db=db,
        connector_id=connector_id,
        connector_data=connector_data
    )


@router.delete(
    "/connectors/{connector_id}",
    status_code=204,
    tags=["Connectors"],
    summary="Delete a specific connector providing its UUID"
)
def delete_connector(connector_id: UUID4, db: Session = Depends(get_db)):
    return crud.delete_connector(db=db, connector_id=connector_id)
