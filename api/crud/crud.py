from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
from fastapi import HTTPException
import logging
from ..models import models
from ..schemas import schemas
from ..utils.helpers import (check_priority_constraint_connector,
                             check_priority_constraint_station,
                             check_connector_count_connector,
                             check_connector_count_station)
from ..utils.auth import get_password_hash

logger = logging.getLogger(__name__)


def create_charging_station_type(db: Session, charging_station_type_data: schemas.ChargingStationTypeCreate):
    try:
        db_charging_station_type = models.ChargingStationType(**charging_station_type_data.dict())
        db.add(db_charging_station_type)
        db.commit()
        db.refresh(db_charging_station_type)
        return db_charging_station_type
    except IntegrityError:
        logger.error("An integrity error occurred while creating a charging station type.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates the database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )
    except Exception:
        logger.error("An error occurred while creating a charging station type.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


def get_charging_station_type(db: Session, charging_station_type_id: UUID4):
    db_charging_station_type = db.query(models.ChargingStationType)\
        .filter(models.ChargingStationType.id == charging_station_type_id)\
        .first()
    if not db_charging_station_type:
        logger.error(f"Charging station type with ID: {charging_station_type_id} not found.")
        raise HTTPException(status_code=404, detail="ChargingStationType instance not found.")
    return db_charging_station_type


def get_charging_station_type_list(
        db: Session,
        plug_count: int,
        min_efficiency: float,
        max_efficiency: float,
        current_type: models.CurrentTypeEnum,
        skip: int,
        limit: int,
):
    query = db.query(models.ChargingStationType)

    if plug_count is not None:
        query = query.filter(models.ChargingStationType.plug_count == plug_count)
    if min_efficiency is not None:
        query = query.filter(models.ChargingStationType.efficiency >= min_efficiency)
    if max_efficiency is not None:
        query = query.filter(models.ChargingStationType.efficiency <= max_efficiency)
    if current_type is not None:
        query = query.filter(models.ChargingStationType.current_type == current_type)

    return query.offset(skip).limit(limit).all()


def update_charging_station_type(
        db: Session,
        charging_station_type_id: UUID4,
        charging_station_type_data: schemas.ChargingStationTypeCreate,
):
    db_charging_station_type = db.query(models.ChargingStationType)\
        .filter(models.ChargingStationType.id == charging_station_type_id)\
        .first()
    if not db_charging_station_type:
        logger.error(f"Charging station type with ID: {charging_station_type_id} not found.")
        raise HTTPException(status_code=404, detail="ChargingStationType instance not found.")
    for key, value in charging_station_type_data.dict().items():
        setattr(db_charging_station_type, key, value)
    try:
        db.commit()
        db.refresh(db_charging_station_type)
        return db_charging_station_type
    except IntegrityError:
        logger.error("An integrity error occurred while updating a charging station type.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates the database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )
    except Exception:
        logger.error("An error occurred while updating a charging station type.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


def delete_charging_station_type(db: Session, charging_station_type_id: UUID4):
    db_charging_station_type = db.query(models.ChargingStationType)\
        .filter(models.ChargingStationType.id == charging_station_type_id)\
        .first()
    if not db_charging_station_type:
        logger.error(f"Charging station type with ID: {charging_station_type_id} not found.")
        raise HTTPException(status_code=404, detail="ChargingStationType instance not found.")
    try:
        db.delete(db_charging_station_type)
        db.commit()
    except IntegrityError:
        logger.error("An integrity error occurred while deleting a charging station type.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Deleting this Charging Station Type violates the database's integrity. "
                   "Make sure that no Charging Stations are assigned to this Type."
        )
    except Exception:
        logger.error("An error occurred while deleting a charging station type.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


def create_charging_station(db: Session, charging_station_data: schemas.ChargingStationCreate):
    logger.info("Checking connector priority constraint...")
    check_priority_constraint_station(charging_station_data.connectors)
    logger.info("Connector priority constraint not violated.")
    logger.info("Checking connector count constraint...")
    check_connector_count_station(db, charging_station_data)
    logger.info("Connector count constraint not violated.")

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
        logger.error("An integrity error occurred while creating a charging station.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates the database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )
    except Exception:
        logger.error("An error occurred while creating a charging station.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


def get_charging_station(db: Session, charging_station_id: UUID4):
    db_charging_station = db.query(models.ChargingStation)\
        .filter(models.ChargingStation.id == charging_station_id)\
        .first()
    if not db_charging_station:
        logger.error(f"Charging station with ID: {charging_station_id} not found.")
        raise HTTPException(status_code=404, detail="ChargingStation instance not found.")

    logger.info("Checking connector count constraint...")
    if db_charging_station.type.plug_count != len(db_charging_station.connectors):
        logger.error(
            f"Unable to retrieve specified charging station. It has {len(db_charging_station.connectors)} "
            f"connectors instead of {db_charging_station.type.plug_count}."
        )
        raise HTTPException(
            status_code=400,
            detail=f"This Charging Station has {len(db_charging_station.connectors)} "
                   f"connectors instead of {db_charging_station.type.plug_count}."
        )
    logger.info("Connector count constraint not violated.")
    return db_charging_station


def get_charging_station_list(
        db: Session,
        plug_count: int,
        min_efficiency: float,
        max_efficiency: float,
        current_type: models.CurrentTypeEnum,
        firmware_version: str,
        skip: int,
        limit: int,
):
    charging_stations = db.query(models.ChargingStation)\
        .join(models.ChargingStationType)\
        .options(joinedload(models.ChargingStation.type),
                 joinedload(models.ChargingStation.connectors))

    if plug_count is not None:
        charging_stations = charging_stations.filter(models.ChargingStationType.plug_count == plug_count)
    if min_efficiency is not None:
        charging_stations = charging_stations.filter(models.ChargingStationType.efficiency >= min_efficiency)
    if max_efficiency is not None:
        charging_stations = charging_stations.filter(models.ChargingStationType.efficiency <= max_efficiency)
    if current_type is not None:
        charging_stations = charging_stations.filter(models.ChargingStationType.current_type == current_type)
    if firmware_version is not None:
        charging_stations = charging_stations.filter(models.ChargingStation.firmware_version == firmware_version)

    logger.info("Checking connector count constraint...")
    for station in charging_stations:
        if len(station.connectors) != station.type.plug_count:
            logger.error("Connector count constraint violation.")
            raise HTTPException(
                status_code=400,
                detail=f"Charging station with id={station.id} has {len(station.connectors)} "
                       f"connectors instead of {station.type.plug_count}."
            )
    logger.info("Connector count constraint not violated.")
    return charging_stations.offset(skip).limit(limit).all()


def update_charging_station(
        db: Session,
        charging_station_id: UUID4,
        charging_station_data: schemas.ChargingStationCreate,
):
    logger.info("Checking connector priority constraint...")
    check_priority_constraint_station(charging_station_data.connectors)
    logger.info("Connector priority constraint not violated.")
    logger.info("Checking connector count constraint...")
    check_connector_count_station(db, charging_station_data)
    logger.info("Connector count constraint not violated.")

    db_charging_station = db.query(models.ChargingStation)\
        .filter(models.ChargingStation.id == charging_station_id)\
        .first()
    if not db_charging_station:
        logger.error(f"Charging station with ID: {charging_station_id} not found.")
        raise HTTPException(status_code=404, detail="ChargingStation instance not found.")

    update_data = charging_station_data.dict(exclude={'connectors'})
    for key, value in update_data.items():
        setattr(db_charging_station, key, value)
    try:
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
        logger.error("An integrity error occurred while updating a charging station.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates the database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )
    except Exception:
        logger.error("An error occurred while updating a charging station.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


def delete_charging_station(db: Session, charging_station_id: UUID4):
    db_charging_station = db.query(models.ChargingStation)\
        .filter(models.ChargingStation.id == charging_station_id)\
        .first()
    if not db_charging_station:
        logger.error(f"Charging station with ID: {charging_station_id} not found.")
        raise HTTPException(status_code=404, detail="ChargingStation instance not found.")
    try:
        db.delete(db_charging_station)
        db.commit()
    except Exception:
        logger.error("An error occurred while deleting a charging station.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


def create_connector(db: Session, connector_data: schemas.ConnectorCreate):
    if connector_data.dict().get('charging_station_id') is not None:
        if connector_data.priority is True:
            logger.info("Checking connector priority constraint...")
            check_priority_constraint_connector(db, connector_data.charging_station_id)
            logger.info("Connector priority constraint not violated.")
        logger.info("Checking connector count constraint...")
        check_connector_count_connector(db, connector_data.charging_station_id)
        logger.info("Connector count constraint not violated.")

    try:
        db_connector = models.Connector(**connector_data.dict())
        db.add(db_connector)
        db.commit()
        db.refresh(db_connector)
        return db_connector
    except IntegrityError:
        logger.error("An integrity error occurred while creating a connector.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates the database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )
    except Exception:
        logger.error("An error occurred while creating a connector.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


def get_connector(db: Session, connector_id: UUID4):
    db_connector = db.query(models.Connector)\
        .filter(models.Connector.id == connector_id)\
        .first()
    if not db_connector:
        logger.error(f"Connector with ID: {connector_id} not found.")
        raise HTTPException(status_code=404, detail="Connector instance not found.")
    return db_connector


def get_connector_list(
        db: Session,
        priority: bool,
        charging_station_id: UUID4,
        skip: int,
        limit: int,
):
    query = db.query(models.Connector)

    if priority is not None:
        query = query.filter(models.Connector.priority == priority)
    if charging_station_id is not None:
        query = query.filter(models.Connector.charging_station_id == charging_station_id)

    return query.offset(skip).limit(limit).all()


def update_connector(
        db: Session,
        connector_id: UUID4,
        connector_data: schemas.ConnectorCreate,
):
    if connector_data.dict().get('charging_station_id') is not None:
        if connector_data.priority is True:
            logger.info("Checking connector priority constraint...")
            check_priority_constraint_connector(db, connector_data.charging_station_id)
            logger.info("Connector priority constraint not violated.")
        logger.info("Checking connector count constraint...")
        check_connector_count_connector(db, connector_data.charging_station_id)
        logger.info("Connector count constraint not violated.")

    db_connector = db.query(models.Connector)\
        .filter(models.Connector.id == connector_id)\
        .first()
    if not db_connector:
        logger.error(f"Connector with ID: {connector_id} not found.")
        raise HTTPException(status_code=404, detail="Connector instance not found.")
    for key, value in connector_data.dict().items():
        setattr(db_connector, key, value)
    try:
        db.commit()
        db.refresh(db_connector)
        return db_connector
    except IntegrityError:
        logger.error("An integrity error occurred while updating a connector.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates database's integrity. "
                   "Make sure that unique and not-null constraints aren't ignored."
        )
    except Exception:
        logger.error("An error occurred while updating a connector.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


def delete_connector(db: Session, connector_id: UUID4):
    db_connector = db.query(models.Connector)\
        .filter(models.Connector.id == connector_id)\
        .first()
    if not db_connector:
        logger.error(f"Connector with ID: {connector_id} not found.")
        raise HTTPException(status_code=404, detail="Connector instance not found.")
    try:
        db.delete(db_connector)
        db.commit()
    except Exception:
        logger.error("An error occurred while deleting a connector.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


def create_user(db: Session, user_data: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if db_user:
        logger.error(f"Username '{user_data.username}' is already used.")
        raise HTTPException(status_code=400, detail=f"Username '{user_data.username}' is already registered.")

    hashed_password = get_password_hash(user_data.password)
    new_user = models.User(username=user_data.username, hashed_password=hashed_password)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        logger.error("An error occurred while creating a new user.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


def update_user(db: Session, username: str, user_data: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        logger.error(f"User '{username}' not found.")
        raise HTTPException(status_code=404, detail=f"User '{username}' not found.")

    db_user.username = user_data.username
    db_user.hashed_password = get_password_hash(user_data.password)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        logger.error("An integrity error occurred while updating user credentials.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Provided data violates the database's integrity. "
                   "Try using another username."
        )
    except Exception:
        logger.error("An error occurred while updating user credentials.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


def delete_user(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        logger.error(f"User '{username}' not found.")
        raise HTTPException(status_code=404, detail=f"User {username} not found.")
    try:
        db.delete(db_user)
        db.commit()
    except Exception:
        logger.error("An error occurred while deleting a user.", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )
