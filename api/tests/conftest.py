import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database.base import Base
from ..models import models
import os
from dotenv import load_dotenv

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL, echo=True)
    testingsessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testingsessionlocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def create_station_type(db_session):
    charging_station_type = models.ChargingStationType(
        name="Test Station Type",
        plug_count=1,
        efficiency=1.1,
        current_type="AC"
    )
    db_session.add(charging_station_type)
    db_session.commit()
    db_session.refresh(charging_station_type)
    return charging_station_type


@pytest.fixture
def create_second_station_type(db_session):
    charging_station_type = models.ChargingStationType(
        name="Test Station Type 2",
        plug_count=2,
        efficiency=90,
        current_type="DC"
    )
    db_session.add(charging_station_type)
    db_session.commit()
    db_session.refresh(charging_station_type)
    return charging_station_type


@pytest.fixture
def create_station(db_session, create_station_type):
    charging_station = models.ChargingStation(
        name="Test Station",
        ip_address="179.148.235.118",
        firmware_version="1.0",
        type_id=create_station_type.id,
    )
    db_session.add(charging_station)
    db_session.commit()
    db_session.refresh(charging_station)
    return charging_station


@pytest.fixture
def create_second_station(db_session, create_second_station_type):
    charging_station = models.ChargingStation(
        name="Test Station 2",
        ip_address="53.72.164.8",
        firmware_version="1.2",
        type_id=create_second_station_type.id,
    )
    db_session.add(charging_station)
    db_session.commit()
    db_session.refresh(charging_station)
    return charging_station


@pytest.fixture
def create_connector(db_session, create_station):
    connector = models.Connector(name="Test Connector", priority=True, charging_station_id=create_station.id)
    db_session.add(connector)
    db_session.commit()
    db_session.refresh(connector)
    return connector


@pytest.fixture
def create_second_connector(db_session, create_second_station):
    connector = models.Connector(name="Test Connector 2", priority=False, charging_station_id=create_second_station.id)
    db_session.add(connector)
    db_session.commit()
    db_session.refresh(connector)
    return connector


@pytest.fixture
def create_third_connector(db_session, create_second_station):
    connector = models.Connector(name="Test Connector 3", priority=True, charging_station_id=create_second_station.id)
    db_session.add(connector)
    db_session.commit()
    db_session.refresh(connector)
    return connector


@pytest.fixture
def create_user(db_session):
    user = models.User(username="admin", hashed_password="supersecretpassword")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def create_second_user(db_session):
    user = models.User(username="admin2", hashed_password="supersecretpassword")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
