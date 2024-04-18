from sqlalchemy.orm import Session
from pydantic import UUID4
from fastapi import HTTPException
from typing import List
import logging
from ..schemas import schemas
from ..models import models

logger = logging.getLogger(__name__)


def check_priority_constraint_connector(db: Session, charging_station_id: UUID4):
    priority_count = db.query(models.Connector).filter(
        models.Connector.charging_station_id == charging_station_id,
        models.Connector.priority.is_(True)
    ).count()

    logger.debug(f"Number of connectors with priority found: {priority_count}.")

    if priority_count > 0:
        logger.error("Connector priority constraint violation.")
        raise HTTPException(
            status_code=400,
            detail="This charging station already has a connector with priority."
        )


def check_priority_constraint_connector_update(db: Session, charging_station_id: UUID4):
    priority_count = db.query(models.Connector).filter(
        models.Connector.charging_station_id == charging_station_id,
        models.Connector.priority.is_(True)
    ).count()

    logger.debug(f"Number of connectors with priority found: {priority_count}.")

    if priority_count > 1:
        logger.error("Connector priority constraint violation.")
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="This charging station already has a connector with priority."
        )


def check_priority_constraint_station(connectors_data: List[schemas.ConnectorCreate]):
    priority_count = sum(1 for connector in connectors_data if connector.priority)

    logger.debug(f"Number of connectors with priority found: {priority_count}.")

    if priority_count > 1:
        logger.error("Connector priority constraint violation.")
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
        logger.error("Charging station not found.")
        raise HTTPException(status_code=404, detail="ChargingStation not found.")

    current_connector_count = len(charging_station.connectors)
    logger.debug(f"Current number of connectors in the charging station: {current_connector_count}.")
    if current_connector_count >= charging_station.type.plug_count:
        logger.error("Connector count constraint violation.")
        raise HTTPException(
            status_code=400,
            detail=f"The number of connectors cannot exceed {charging_station.type.plug_count} "
                   f"in this Charging Station."
        )


def check_connector_count_connector_update(db: Session, charging_station_id: UUID4):
    charging_station = db.query(models.ChargingStation)\
        .filter(models.ChargingStation.id == charging_station_id)\
        .join(models.ChargingStationType)\
        .one_or_none()
    if not charging_station:
        logger.error("Charging station not found.")
        raise HTTPException(status_code=404, detail="ChargingStation not found.")

    current_connector_count = len(charging_station.connectors)
    logger.debug(f"Current number of connectors in the charging station: {current_connector_count}.")
    if current_connector_count > charging_station.type.plug_count:
        logger.error("Connector count constraint violation.")
        db.rollback()
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
        logger.error("Charging station not found.")
        raise HTTPException(status_code=404, detail="ChargingStationType not found.")

    connector_count = len(charging_station_data.connectors)
    logger.debug(f"Current number of connectors in the charging station: {connector_count}.")
    if connector_count != charging_station_type.plug_count:
        logger.error("Connector count constraint violation.")
        raise HTTPException(
            status_code=400,
            detail=f"The number of connectors must equal {charging_station_type.plug_count} in this Charging Station."
        )
