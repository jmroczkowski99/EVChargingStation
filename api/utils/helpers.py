from sqlalchemy.orm import Session
from pydantic import UUID4
from fastapi import HTTPException
from typing import List
from ..schemas import schemas
from ..models import models


def check_priority_constraint_connector(db: Session, charging_station_id: UUID4):
    priority_count = db.query(models.Connector).filter(
        models.Connector.charging_station_id == charging_station_id,
        models.Connector.priority.is_(True)
    ).count()
    if priority_count > 0:
        raise HTTPException(
            status_code=400,
            detail="This charging station already has a connector with priority."
        )


def check_priority_constraint_station(db: Session, connectors_data: List[schemas.ConnectorCreate]):
    priority_count = sum(1 for connector in connectors_data if connector.priority)
    if priority_count > 1:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Only one connector in each Charging Station can have priority."
        )


def check_connector_count_connector(db: Session, charging_station_id: UUID4):
    charging_station = db.query(models.ChargingStation)\
        .filter(models.ChargingStation.id == charging_station_id)\
        .join(models.ChargingStationType)\
        .one_or_none()
    if not charging_station:
        raise HTTPException(status_code=404, detail="ChargingStation not found.")

    current_connector_count = len(charging_station.connectors)
    if current_connector_count >= charging_station.type.plug_count:
        raise HTTPException(
            status_code=400,
            detail=f"The number of connectors cannot exceed {charging_station.type.plug_count} "
                   f"in this Charging Station."
        )


def check_connector_count_station(db: Session, charging_station_data: schemas.ChargingStationCreate):
    charging_station_type = db.query(models.ChargingStationType).\
        filter(models.ChargingStationType.id == charging_station_data.type_id).\
        one_or_none()
    if not charging_station_type:
        raise HTTPException(status_code=404, detail="ChargingStationType not found.")

    connector_count = len(charging_station_data.connectors)
    if connector_count != charging_station_type.plug_count:
        raise HTTPException(
            status_code=400,
            detail=f"The number of connectors must equal {charging_station_type.plug_count} in this Charging Station."
        )
