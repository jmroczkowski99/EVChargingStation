import pytest
from fastapi import HTTPException
from ..utils.helpers import (
    check_priority_constraint_connector_update,
    check_connector_count_connector_update,
    check_connector_count_station,
    check_priority_constraint_station,
    check_connector_count_connector,
    check_priority_constraint_connector
)
from ..models.models import Connector
from ..schemas import schemas


class TestPriorityConstraint:
    def test_priority_constraint_connector(self, db_session, create_station, create_connector):
        with pytest.raises(HTTPException) as exc_info:
            check_priority_constraint_connector(db_session, create_station.id)

        assert exc_info.value.status_code == 400
        assert "This charging station already has a connector with priority" in exc_info.value.detail

    def test_priority_constraint_connector_not_raised(self, db_session, create_station):
        check_priority_constraint_connector(db_session, create_station.id)

    def test_priority_constraint_connector_update(self, db_session, create_second_station, create_third_connector):
        connector = Connector(name="Test Connector", priority=True, charging_station_id=create_second_station.id)
        db_session.add(connector)
        db_session.commit()
        with pytest.raises(HTTPException) as exc_info:
            check_priority_constraint_connector_update(db_session, create_second_station.id)

        assert exc_info.value.status_code == 400
        assert "This charging station already has a connector with priority" in exc_info.value.detail

    def test_priority_constraint_connector_update_not_raised(
            self,
            db_session,
            create_second_station,
            create_third_connector
    ):
        connector = Connector(name="Test Connector", priority=False, charging_station_id=create_second_station.id)
        db_session.add(connector)
        db_session.commit()
        check_priority_constraint_connector_update(db_session, create_second_station.id)

    def test_priority_constraint_station(self):
        connector_data = [
            schemas.ConnectorCreate(name="Test Connector", priority=True),
            schemas.ConnectorCreate(name="Test Connector 2", priority=True)
        ]
        with pytest.raises(HTTPException) as exc_info:
            check_priority_constraint_station(connector_data)

        assert exc_info.value.status_code == 400
        assert "Only one connector in each Charging Station can have priority." in exc_info.value.detail

    def test_priority_constraint_station_not_raised(self):
        connector_data = [
            schemas.ConnectorCreate(name="Test Connector", priority=False),
            schemas.ConnectorCreate(name="Test Connector 2", priority=True)
        ]
        check_priority_constraint_station(connector_data)


class TestCountConstraint:
    def test_count_constraint_connector_wrong_id(self, db_session, create_station):
        with pytest.raises(HTTPException) as exc_info:
            check_connector_count_connector(db_session, "bf77f736-db94-447f-8903-48345e03f5e2")

        assert exc_info.value.status_code == 404
        assert "ChargingStation not found." in exc_info.value.detail

    def test_count_constraint_connector(self, db_session, create_station, create_connector):
        with pytest.raises(HTTPException) as exc_info:
            check_connector_count_connector(db_session, create_station.id)

        assert exc_info.value.status_code == 400
        assert "cannot exceed" in exc_info.value.detail

    def test_count_constraint_connector_not_raised(self, db_session, create_station):
        check_connector_count_connector(db_session, create_station.id)

    def test_count_constraint_connector_update_wrong_id(self, db_session, create_station):
        with pytest.raises(HTTPException) as exc_info:
            check_connector_count_connector_update(db_session, "bf77f736-db94-447f-8903-48345e03f5e2")

        assert exc_info.value.status_code == 404
        assert "ChargingStation not found." in exc_info.value.detail

    def test_count_constraint_connector_update(self, db_session, create_station, create_connector):
        connector = Connector(name="Test Connector 2", priority=False, charging_station_id=create_station.id)
        db_session.add(connector)
        db_session.commit()
        with pytest.raises(HTTPException) as exc_info:
            check_connector_count_connector_update(db_session, create_station.id)

        assert exc_info.value.status_code == 400
        assert "cannot exceed" in exc_info.value.detail

    def test_count_constraint_connector_update_not_raised(self, db_session, create_station, create_connector):
        check_connector_count_connector_update(db_session, create_station.id)

    def test_count_constraint_station(self, db_session, create_station_type):
        connectors = [
            schemas.ConnectorCreateWithStation(name="Test Connector", priority=False),
            schemas.ConnectorCreateWithStation(name="Test Connector 2", priority=False)
        ]
        station_data = schemas.ChargingStationCreate(
            name="Test Station",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id=create_station_type.id,
            connectors=connectors
        )

        with pytest.raises(HTTPException) as exc_info:
            check_connector_count_station(db_session, station_data)
        assert exc_info.value.status_code == 400
        assert "must equal" in exc_info.value.detail

    def test_count_constraint_station_wrong_type_id(self, db_session, create_station_type):
        connectors = [
            schemas.ConnectorCreateWithStation(name="Test Connector", priority=False),
            schemas.ConnectorCreateWithStation(name="Test Connector 2", priority=False)
        ]
        station_data = schemas.ChargingStationCreate(
            name="Test Station",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id="bf77f736-db94-447f-8903-48345e03f5e2",
            connectors=connectors
        )

        with pytest.raises(HTTPException) as exc_info:
            check_connector_count_station(db_session, station_data)
        assert exc_info.value.status_code == 404
        assert "ChargingStationType not found." in exc_info.value.detail

    def test_count_constraint_station_not_raised(self, db_session, create_station_type):
        connectors = [
            schemas.ConnectorCreateWithStation(name="Test Connector", priority=False),
        ]
        station_data = schemas.ChargingStationCreate(
            name="Test Station",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id=create_station_type.id,
            connectors=connectors
        )
        check_connector_count_station(db_session, station_data)
