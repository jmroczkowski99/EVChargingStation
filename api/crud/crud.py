from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
from fastapi import HTTPException
from ..models import models
from ..schemas import schemas
from ..utils.helpers import (check_priority_constraint_connector,
                             check_priority_constraint_station,
                             check_connector_count_connector,
                             check_connector_count_station)


def create_charging_station_type(db: Session, charging_station_type_data: schemas.ChargingStationTypeCreate):
    try:
        db_charging_station_type = models.ChargingStationType(**charging_station_type_data.dict())
        db.add(db_charging_station_type)
        db.commit()
        db.refresh(db_charging_station_type)
        return db_charging_station_type
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates the database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )


def get_charging_station_type(db: Session, charging_station_type_id: UUID4):
    db_charging_station_type = db.query(models.ChargingStationType)\
        .filter(models.ChargingStationType.id == charging_station_type_id)\
        .first()
    if not db_charging_station_type:
        raise HTTPException(status_code=404, detail="ChargingStationType instance not found.")
    return db_charging_station_type


def get_charging_station_type_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ChargingStationType).offset(skip).limit(limit).all()


def update_charging_station_type(
        db: Session,
        charging_station_type_id: UUID4,
        charging_station_type_data: schemas.ChargingStationTypeCreate,
):
    try:
        db_charging_station_type = db.query(models.ChargingStationType)\
            .filter(models.ChargingStationType.id == charging_station_type_id)\
            .first()
        if not db_charging_station_type:
            raise HTTPException(status_code=404, detail="ChargingStationType instance not found.")
        for key, value in charging_station_type_data.dict().items():
            setattr(db_charging_station_type, key, value)
        db.commit()
        db.refresh(db_charging_station_type)
        return db_charging_station_type
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates the database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )


def delete_charging_station_type(db: Session, charging_station_type_id: UUID4):
    try:
        db_charging_station_type = db.query(models.ChargingStationType)\
            .filter(models.ChargingStationType.id == charging_station_type_id)\
            .first()
        if db_charging_station_type:
            db.delete(db_charging_station_type)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="ChargingStationType instance not found.")
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Deleting this Charging Station Type violates the database's integrity. "
                   "Make sure that no Charging Stations are assigned to this Type."
        )


def create_charging_station(db: Session, charging_station_data: schemas.ChargingStationCreate):
    check_priority_constraint_station(db, charging_station_data.connectors)
    check_connector_count_station(db, charging_station_data)

    try:
        db_charging_station = models.ChargingStation(**charging_station_data.dict(exclude={'connectors'}))
        db.add(db_charging_station)
        db.flush()

        connectors_data = charging_station_data.connectors

        for connector_data in connectors_data:
            connector = models.Connector(**connector_data.dict())
            db_charging_station.connectors.append(connector)

        db.commit()
        db.refresh(db_charging_station)
        return db_charging_station
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates the database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )


def get_charging_station(db: Session, charging_station_id: UUID4):
    db_charging_station = db.query(models.ChargingStation)\
        .filter(models.ChargingStation.id == charging_station_id)\
        .first()
    if not db_charging_station:
        raise HTTPException(status_code=404, detail="ChargingStation instance not found.")
    if db_charging_station.type.plug_count != len(db_charging_station.connectors):
        raise HTTPException(
            status_code=400,
            detail=f"This Charging Station has {len(db_charging_station.connectors)} "
                   f"connectors instead of {db_charging_station.type.plug_count}."
        )
    return db_charging_station


def get_charging_station_list(db: Session, skip: int = 0, limit: int = 100):
    charging_stations = db.query(models.ChargingStation)\
        .options(joinedload(models.ChargingStation.type),
                 joinedload(models.ChargingStation.connectors))\
        .offset(skip).limit(limit).all()
    for station in charging_stations:
        if len(station.connectors) != station.type.plug_count:
            raise HTTPException(
                status_code=400,
                detail=f"Charging station with id={station.id} has {len(station.connectors)} "
                       f"connectors instead of {station.type.plug_count}."
            )
    return charging_stations


def update_charging_station(
        db: Session,
        charging_station_id: UUID4,
        charging_station_data: schemas.ChargingStationCreate,
):
    check_priority_constraint_station(db, charging_station_data.connectors)
    check_connector_count_station(db, charging_station_data)

    try:
        db_charging_station = db.query(models.ChargingStation)\
            .filter(models.ChargingStation.id == charging_station_id)\
            .first()
        if not db_charging_station:
            raise HTTPException(status_code=404, detail="ChargingStation instance not found.")

        update_data = charging_station_data.dict(exclude={'connectors'})
        for key, value in update_data.items():
            setattr(db_charging_station, key, value)

        existing_connectors = db_charging_station.connectors
        for connector in existing_connectors:
            db.delete(connector)
            db.flush()

        connectors_data = charging_station_data.connectors
        for connector_data in connectors_data:
            connector = models.Connector(**connector_data.dict())
            db_charging_station.connectors.append(connector)

        db.commit()
        db.refresh(db_charging_station)
        return db_charging_station
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates the database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )


def delete_charging_station(db: Session, charging_station_id: UUID4):
    db_charging_station = db.query(models.ChargingStation)\
        .filter(models.ChargingStation.id == charging_station_id)\
        .first()
    if db_charging_station:
        db.delete(db_charging_station)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="ChargingStation instance not found.")


def create_connector(db: Session, connector_data: schemas.ConnectorCreate):
    if connector_data.dict().get('charging_station_id') is not None:
        if connector_data.priority is True:
            check_priority_constraint_connector(db, connector_data.charging_station_id)
        check_connector_count_connector(db, connector_data.charging_station_id)

    try:
        db_connector = models.Connector(**connector_data.dict())
        db.add(db_connector)
        db.commit()
        db.refresh(db_connector)
        return db_connector
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates the database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )


def get_connector(db: Session, connector_id: UUID4):
    db_connector = db.query(models.Connector)\
        .filter(models.Connector.id == connector_id)\
        .first()
    if not db_connector:
        raise HTTPException(status_code=404, detail="Connector instance not found.")
    return db_connector


def get_connector_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Connector).offset(skip).limit(limit).all()


def update_connector(
        db: Session,
        connector_id: UUID4,
        connector_data: schemas.ConnectorCreate,
):
    if connector_data.dict().get('charging_station_id') is not None:
        if connector_data.priority is True:
            check_priority_constraint_connector(db, connector_data.charging_station_id)
        check_connector_count_connector(db, connector_data.charging_station_id)

    try:
        db_connector = db.query(models.Connector)\
            .filter(models.Connector.id == connector_id)\
            .first()
        if not db_connector:
            raise HTTPException(status_code=404, detail="Connector instance not found.")
        for key, value in connector_data.dict().items():
            setattr(db_connector, key, value)
        db.commit()
        db.refresh(db_connector)
        return db_connector
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )


def delete_connector(db: Session, connector_id: UUID4):
    db_connector = db.query(models.Connector)\
        .filter(models.Connector.id == connector_id)\
        .first()
    if db_connector:
        db.delete(db_connector)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Connector instance not found.")
