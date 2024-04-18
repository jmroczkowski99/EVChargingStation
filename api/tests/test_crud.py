import pytest
from fastapi import HTTPException
from ..crud import crud
from ..schemas import schemas
from ..models.models import CurrentTypeEnum, User


class TestChargingStationTypeCrud:
    def test_create_charging_station_type_success(self, db_session):
        data = schemas.ChargingStationTypeCreate(
            name="Test Station Type",
            plug_count=1,
            efficiency=1.1,
            current_type="AC"
        )

        charging_station_type = crud.create_charging_station_type(db_session, data)

        assert charging_station_type.name == "Test Station Type"
        assert charging_station_type.plug_count == 1
        assert charging_station_type.efficiency == 1.1
        assert charging_station_type.current_type == CurrentTypeEnum.AC
        assert charging_station_type.charging_stations == []

    def test_create_charging_station_type_not_unique(self, db_session, create_station_type):
        data = schemas.ChargingStationTypeCreate(
            name="Test Station Type",
            plug_count=1,
            efficiency=1.1,
            current_type="AC"
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.create_charging_station_type(db_session, data)

        assert exc_info.value.status_code == 400
        assert "violates the database's integrity" in exc_info.value.detail

    def test_get_charging_station_type_success(self, db_session, create_station_type):
        charging_station_type = crud.get_charging_station_type(db_session, create_station_type.id)

        assert charging_station_type.name == create_station_type.name
        assert charging_station_type.plug_count == create_station_type.plug_count
        assert charging_station_type.efficiency == create_station_type.efficiency
        assert charging_station_type.current_type == create_station_type.current_type
        assert charging_station_type.charging_stations == create_station_type.charging_stations

    def test_get_charging_station_type_wrong_id(self, db_session, create_station_type):
        with pytest.raises(HTTPException) as exc_info:
            crud.get_charging_station_type(db_session, "a73ee835-1201-4888-9d3a-911f48958b42")

        assert exc_info.value.status_code == 404
        assert "ChargingStationType instance not found." in exc_info.value.detail

    def test_get_charging_station_list_no_params(self, db_session, create_station_type, create_second_station_type):
        charging_station_type_list = crud.get_charging_station_type_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=None,
            current_type=None,
            skip=None,
            limit=None
        )

        assert len(charging_station_type_list) == 2

    def test_get_charging_station_list_plug_count(self, db_session, create_station_type, create_second_station_type):
        charging_station_type_list = crud.get_charging_station_type_list(
            db=db_session,
            plug_count=1,
            min_efficiency=None,
            max_efficiency=None,
            current_type=None,
            skip=None,
            limit=None
        )

        assert len(charging_station_type_list) == 1

    def test_get_charging_station_list_min_eff(self, db_session, create_station_type, create_second_station_type):
        charging_station_type_list = crud.get_charging_station_type_list(
            db=db_session,
            plug_count=None,
            min_efficiency=80,
            max_efficiency=None,
            current_type=None,
            skip=None,
            limit=None
        )

        assert len(charging_station_type_list) == 1

    def test_get_charging_station_list_max_eff(self, db_session, create_station_type, create_second_station_type):
        charging_station_type_list = crud.get_charging_station_type_list(
            db=db_session,
            plug_count=None,
            min_efficiency=80,
            max_efficiency=82,
            current_type=None,
            skip=None,
            limit=None
        )

        assert len(charging_station_type_list) == 0

    def test_get_charging_station_list_current(self, db_session, create_station_type, create_second_station_type):
        charging_station_type_list = crud.get_charging_station_type_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=None,
            current_type="DC",
            skip=None,
            limit=None
        )

        assert len(charging_station_type_list) == 1

    def test_get_charging_station_list_skip(self, db_session, create_station_type, create_second_station_type):
        charging_station_type_list = crud.get_charging_station_type_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=None,
            current_type=None,
            skip=1,
            limit=None
        )

        assert len(charging_station_type_list) == 1

    def test_get_charging_station_list_limit(self, db_session, create_station_type, create_second_station_type):
        charging_station_type_list = crud.get_charging_station_type_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=None,
            current_type=None,
            skip=None,
            limit=1
        )

        assert len(charging_station_type_list) == 1

    def test_update_charging_station_type_success(self, db_session, create_station_type):
        data = schemas.ChargingStationTypeCreate(
            name="Test Station Type Updated",
            plug_count=16,
            efficiency=99.99,
            current_type="DC"
        )

        charging_station_type = crud.update_charging_station_type(db_session, create_station_type.id, data)

        assert charging_station_type.name == "Test Station Type Updated"
        assert charging_station_type.plug_count == 16
        assert charging_station_type.efficiency == 99.99
        assert charging_station_type.current_type == CurrentTypeEnum.DC
        assert charging_station_type.charging_stations == []

    def test_update_charging_station_type_wrong_id(self, db_session, create_station_type):
        data = schemas.ChargingStationTypeCreate(
            name="Test Station Type Updated",
            plug_count=16,
            efficiency=99.99,
            current_type="DC"
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.update_charging_station_type(db_session, "a73ee835-1201-4888-9d3a-911f48958b42", data)

        assert exc_info.value.status_code == 404
        assert "ChargingStationType instance not found." in exc_info.value.detail

    def test_update_charging_station_type_not_unique(self, db_session, create_station_type, create_second_station_type):
        data = schemas.ChargingStationTypeCreate(
            name=create_second_station_type.name,
            plug_count=16,
            efficiency=99.99,
            current_type="DC"
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.update_charging_station_type(db_session, create_station_type.id, data)

        assert exc_info.value.status_code == 400
        assert "violates the database's integrity" in exc_info.value.detail

    def test_delete_charging_station_type_success(self, db_session, create_station_type):
        crud.delete_charging_station_type(db_session, create_station_type.id)

        charging_station_type_list = crud.get_charging_station_type_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=None,
            current_type=None,
            skip=None,
            limit=None
        )

        assert len(charging_station_type_list) == 0

    def test_delete_charging_station_type_wrong_id(self, db_session, create_station_type):
        with pytest.raises(HTTPException) as exc_info:
            crud.delete_charging_station_type(db_session, "a73ee835-1201-4888-9d3a-911f48958b42")

        assert exc_info.value.status_code == 404
        assert "ChargingStationType instance not found." in exc_info.value.detail

    def test_delete_charging_station_type_assigned_type(self, db_session, create_station_type, create_station):
        with pytest.raises(HTTPException) as exc_info:
            crud.delete_charging_station_type(db_session, create_station_type.id)

        assert exc_info.value.status_code == 400
        assert "Make sure that no Charging Stations are assigned to this Type." in exc_info.value.detail


class TestChargingStationCrud:
    def test_create_charging_station_success(self, db_session, create_station_type):
        data = schemas.ChargingStationCreate(
            name="Test Station",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id=create_station_type.id,
            connectors=[schemas.ConnectorCreateWithStation(name="Test Connector", priority=True)]
        )

        charging_station = crud.create_charging_station(db_session, data)

        assert charging_station.name == "Test Station"
        assert charging_station.ip_address == "179.148.235.118"
        assert charging_station.firmware_version == "1.0"
        assert charging_station.device_id
        assert charging_station.type_id == create_station_type.id
        assert len(charging_station.connectors) == 1

    def test_create_charging_station_not_unique(self, db_session, create_station_type, create_station):
        data = schemas.ChargingStationCreate(
            name="Test Station",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id=create_station_type.id,
            connectors=[schemas.ConnectorCreateWithStation(name="Test Connector", priority=True)]
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.create_charging_station(db_session, data)

        assert exc_info.value.status_code == 400
        assert "violates the database's integrity" in exc_info.value.detail

    def test_create_charging_station_connector_count_constraint(self, db_session, create_station_type):
        data = schemas.ChargingStationCreate(
            name="Test Station",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id=create_station_type.id,
            connectors=[
                schemas.ConnectorCreateWithStation(name="Test Connector", priority=True),
                schemas.ConnectorCreateWithStation(name="Test Connector 2", priority=False)
            ]
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.create_charging_station(db_session, data)

        assert exc_info.value.status_code == 400
        assert "The number of connectors must equal" in exc_info.value.detail

    def test_create_charging_station_connector_priority_constraint(self, db_session, create_second_station_type):
        data = schemas.ChargingStationCreate(
            name="Test Station",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id=create_second_station_type.id,
            connectors=[
                schemas.ConnectorCreateWithStation(name="Test Connector", priority=True),
                schemas.ConnectorCreateWithStation(name="Test Connector 2", priority=True)
            ]
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.create_charging_station(db_session, data)

        assert exc_info.value.status_code == 400
        assert "Only one connector in each Charging Station can have priority." in exc_info.value.detail

    def test_get_charging_station_success(self, db_session, create_station, create_connector):
        charging_station = crud.get_charging_station(db_session, create_station.id)

        assert charging_station.name == create_station.name
        assert charging_station.type_id == create_station.type_id
        assert charging_station.device_id == create_station.device_id
        assert charging_station.ip_address == create_station.ip_address
        assert charging_station.firmware_version == create_station.firmware_version
        assert charging_station.connectors == create_station.connectors

    def test_get_charging_station_wrong_id(self, db_session, create_station, create_connector):
        with pytest.raises(HTTPException) as exc_info:
            crud.get_charging_station(db_session, "a73ee835-1201-4888-9d3a-911f48958b42")

        assert exc_info.value.status_code == 404
        assert "ChargingStation instance not found." in exc_info.value.detail

    def test_get_charging_station_wrong_connector_count(self, db_session, create_station):
        with pytest.raises(HTTPException) as exc_info:
            crud.get_charging_station(db_session, create_station.id)

        assert exc_info.value.status_code == 400
        assert f"This Charging Station has {len(create_station.connectors)} " \
               f"connectors instead of {create_station.type.plug_count}." in exc_info.value.detail

    def test_get_charging_station_list_no_params(
            self,
            db_session,
            create_station,
            create_second_station,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        charging_station_list = crud.get_charging_station_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=None,
            current_type=None,
            firmware_version=None,
            skip=None,
            limit=None
        )

        assert len(charging_station_list) == 2

    def test_get_charging_station_list_plug_count(
            self,
            db_session,
            create_station,
            create_second_station,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        charging_station_list = crud.get_charging_station_list(
            db=db_session,
            plug_count=1,
            min_efficiency=None,
            max_efficiency=None,
            current_type=None,
            firmware_version=None,
            skip=None,
            limit=None
        )

        assert len(charging_station_list) == 1

    def test_get_charging_station_list_min_eff(
            self,
            db_session,
            create_station,
            create_second_station,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        charging_station_list = crud.get_charging_station_list(
            db=db_session,
            plug_count=None,
            min_efficiency=80,
            max_efficiency=None,
            current_type=None,
            firmware_version=None,
            skip=None,
            limit=None
        )

        assert len(charging_station_list) == 1

    def test_get_charging_station_list_max_eff(
            self,
            db_session,
            create_station,
            create_second_station,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        charging_station_list = crud.get_charging_station_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=80,
            current_type=None,
            firmware_version=None,
            skip=None,
            limit=None
        )

        assert len(charging_station_list) == 1

    def test_get_charging_station_list_current_type(
            self,
            db_session,
            create_station,
            create_second_station,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        charging_station_list = crud.get_charging_station_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=None,
            current_type="AC",
            firmware_version=None,
            skip=None,
            limit=None
        )

        assert len(charging_station_list) == 1

    def test_get_charging_station_list_firmware(
            self,
            db_session,
            create_station,
            create_second_station,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        charging_station_list = crud.get_charging_station_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=None,
            current_type=None,
            firmware_version="1.0",
            skip=None,
            limit=None
        )

        assert len(charging_station_list) == 1

    def test_get_charging_station_list_skip(
            self,
            db_session,
            create_station,
            create_second_station,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        charging_station_list = crud.get_charging_station_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=None,
            current_type=None,
            firmware_version=None,
            skip=1,
            limit=None
        )

        assert len(charging_station_list) == 1

    def test_get_charging_station_list_limit(
            self,
            db_session,
            create_station,
            create_second_station,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        charging_station_list = crud.get_charging_station_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=None,
            current_type=None,
            firmware_version=None,
            skip=None,
            limit=1
        )

        assert len(charging_station_list) == 1

    def test_get_charging_station_list_wrong_connector_count(
            self,
            db_session,
            create_station,
            create_second_station,
            create_connector,
            create_second_connector,
    ):
        with pytest.raises(HTTPException) as exc_info:
            crud.get_charging_station_list(
                db=db_session,
                plug_count=None,
                min_efficiency=None,
                max_efficiency=None,
                current_type=None,
                firmware_version=None,
                skip=None,
                limit=None
            )

        assert exc_info.value.status_code == 400
        assert f"Charging station with id={create_second_station.id} has {len(create_second_station.connectors)} "\
               f"connectors instead of {create_second_station.type.plug_count}." in exc_info.value.detail

    def test_update_charging_station_success(self, db_session, create_station_type, create_station):
        data = schemas.ChargingStationCreate(
            name="Test Station Updated",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id=create_station_type.id,
            connectors=[schemas.ConnectorCreateWithStation(name="Test Connector", priority=True)]
        )

        charging_station = crud.update_charging_station(db_session, create_station.id, data)

        assert charging_station.name == "Test Station Updated"
        assert charging_station.ip_address == "179.148.235.118"
        assert charging_station.firmware_version == "1.0"
        assert charging_station.device_id
        assert charging_station.type_id == create_station_type.id
        assert len(charging_station.connectors) == 1

    def test_update_charging_station_wrong_id(self, db_session, create_station_type, create_station):
        data = schemas.ChargingStationCreate(
            name="Test Station Updated",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id=create_station_type.id,
            connectors=[schemas.ConnectorCreateWithStation(name="Test Connector", priority=True)]
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.update_charging_station(db_session, "a73ee835-1201-4888-9d3a-911f48958b42", data)

        assert exc_info.value.status_code == 404
        assert "ChargingStation instance not found." in exc_info.value.detail

    def test_update_charging_station_not_unique(
            self,
            db_session,
            create_station_type,
            create_station,
            create_second_station
    ):
        data = schemas.ChargingStationCreate(
            name="Test Station 2",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id=create_station_type.id,
            connectors=[schemas.ConnectorCreateWithStation(name="Test Connector", priority=True)]
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.update_charging_station(db_session, create_station.id, data)

        assert exc_info.value.status_code == 400
        assert "violates the database's integrity." in exc_info.value.detail

    def test_update_charging_station_connector_count_constraint(
            self,
            db_session,
            create_station_type,
            create_station,
    ):
        data = schemas.ChargingStationCreate(
            name="Test Station 2",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id=create_station_type.id,
            connectors=[
                schemas.ConnectorCreateWithStation(name="Test Connector", priority=True),
                schemas.ConnectorCreateWithStation(name="Test Connector 2", priority=False)
            ]
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.update_charging_station(db_session, create_station.id, data)

        assert exc_info.value.status_code == 400
        assert "The number of connectors must equal" in exc_info.value.detail

    def test_update_charging_station_connector_priority_constraint(
            self,
            db_session,
            create_second_station_type,
            create_station,
    ):
        data = schemas.ChargingStationCreate(
            name="Test Station 2",
            ip_address="179.148.235.118",
            firmware_version="1.0",
            type_id=create_second_station_type.id,
            connectors=[
                schemas.ConnectorCreateWithStation(name="Test Connector", priority=True),
                schemas.ConnectorCreateWithStation(name="Test Connector 2", priority=True)
            ]
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.update_charging_station(db_session, create_station.id, data)

        assert exc_info.value.status_code == 400
        assert "Only one connector in each Charging Station can have priority." in exc_info.value.detail

    def test_delete_charging_station_success(self, db_session, create_station):
        crud.delete_charging_station(db_session, create_station.id)

        charging_station_list = crud.get_charging_station_list(
            db=db_session,
            plug_count=None,
            min_efficiency=None,
            max_efficiency=None,
            current_type=None,
            firmware_version=None,
            skip=None,
            limit=None
        )

        assert len(charging_station_list) == 0

    def test_delete_charging_station_wrong_id(self, db_session, create_station):
        with pytest.raises(HTTPException) as exc_info:
            crud.delete_charging_station(db_session, "a73ee835-1201-4888-9d3a-911f48958b42")

        assert exc_info.value.status_code == 404
        assert "ChargingStation instance not found." in exc_info.value.detail


class TestConnectorCrud:
    def test_create_connector_success(self, db_session, create_station):
        data = schemas.ConnectorCreate(
            name="Test Connector",
            priority=True,
            charging_station_id=create_station.id
        )

        connector = crud.create_connector(db_session, data)

        assert connector.name == "Test Connector"
        assert connector.priority is True
        assert connector.charging_station_id == create_station.id

    def test_create_connector_no_station_success(self, db_session):
        data = schemas.ConnectorCreate(
            name="Test Connector",
            priority=True,
        )

        connector = crud.create_connector(db_session, data)

        assert connector.name == "Test Connector"
        assert connector.priority is True
        assert connector.charging_station_id is None

    def test_create_connector_not_unique(self, db_session, create_connector):
        data = schemas.ConnectorCreate(
            name="Test Connector",
            priority=True
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.create_connector(db_session, data)

        assert exc_info.value.status_code == 400
        assert "violates the database's integrity." in exc_info.value.detail

    def test_create_connector_priority_constraint(self, db_session, create_second_station, create_third_connector):
        data = schemas.ConnectorCreate(
            name="Test Connector",
            priority=True,
            charging_station_id=create_second_station.id
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.create_connector(db_session, data)

        assert exc_info.value.status_code == 400
        assert "This charging station already has a connector with priority." in exc_info.value.detail

    def test_create_connector_count_constraint(self, db_session, create_station, create_connector):
        data = schemas.ConnectorCreate(
            name="Test Connector priority",
            priority=False,
            charging_station_id=create_station.id
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.create_connector(db_session, data)

        assert exc_info.value.status_code == 400
        assert "The number of connectors cannot exceed" in exc_info.value.detail

    def test_get_connector_success(self, db_session, create_connector):
        connector = crud.get_connector(db_session, create_connector.id)

        assert connector.name == create_connector.name
        assert connector.priority == create_connector.priority
        assert connector.charging_station_id == create_connector.charging_station_id

    def test_get_connector_wrong_id(self, db_session, create_connector):
        with pytest.raises(HTTPException) as exc_info:
            crud.get_connector(db_session, "a73ee835-1201-4888-9d3a-911f48958b42")

        assert exc_info.value.status_code == 404
        assert "Connector instance not found." in exc_info.value.detail

    def test_get_connector_list_no_params(self, db_session, create_station, create_connector, create_second_connector):
        connector_list = crud.get_connector_list(
            db=db_session,
            priority=None,
            charging_station_id=None,
            skip=None,
            limit=None
        )

        assert len(connector_list) == 2

    def test_get_connector_list_priority(self, db_session, create_station, create_connector, create_second_connector):
        connector_list = crud.get_connector_list(
            db=db_session,
            priority=True,
            charging_station_id=None,
            skip=None,
            limit=None
        )

        assert len(connector_list) == 1

    def test_get_connector_list_charging_station_id(
            self,
            db_session,
            create_station,
            create_connector,
            create_second_connector
    ):
        connector_list = crud.get_connector_list(
            db=db_session,
            priority=None,
            charging_station_id=create_station.id,
            skip=None,
            limit=None
        )

        assert len(connector_list) == 1

    def test_get_connector_list_skip(self, db_session, create_station, create_connector, create_second_connector):
        connector_list = crud.get_connector_list(
            db=db_session,
            priority=None,
            charging_station_id=None,
            skip=1,
            limit=None
        )

        assert len(connector_list) == 1

    def test_get_connector_list_limit(self, db_session, create_station, create_connector, create_second_connector):
        connector_list = crud.get_connector_list(
            db=db_session,
            priority=None,
            charging_station_id=None,
            skip=None,
            limit=1
        )

        assert len(connector_list) == 1

    def test_update_connector_success(self, db_session, create_station, create_connector):
        data = schemas.ConnectorCreate(
            name="Test Connector Updated",
            priority=True,
            charging_station_id=create_station.id
        )

        connector = crud.update_connector(db_session, create_connector.id, data)

        assert connector.name == "Test Connector Updated"
        assert connector.priority is True
        assert connector.charging_station_id == create_station.id

    def test_update_connector_success_no_charging_station(self, db_session, create_connector):
        data = schemas.ConnectorCreate(
            name="Test Connector Updated",
            priority=True,
        )

        connector = crud.update_connector(db_session, create_connector.id, data)

        assert connector.name == "Test Connector Updated"
        assert connector.priority is True
        assert connector.charging_station_id is None

    def test_update_connector_wrong_id(self, db_session, create_connector):
        data = schemas.ConnectorCreate(
            name="Test Connector Updated",
            priority=True,
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.update_connector(db_session, "a73ee835-1201-4888-9d3a-911f48958b42", data)

        assert exc_info.value.status_code == 404
        assert "Connector instance not found." in exc_info.value.detail

    def test_update_connector_not_unique(self, db_session, create_connector, create_second_connector):
        data = schemas.ConnectorCreate(
            name="Test Connector 2",
            priority=True,
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.update_connector(db_session, create_connector.id, data)

        assert exc_info.value.status_code == 400
        assert "violates database's integrity." in exc_info.value.detail

    def test_update_connector_priority_constraint(
            self,
            db_session,
            create_connector,
            create_second_station,
            create_third_connector
    ):
        data = schemas.ConnectorCreate(
            name="Test Connector",
            priority=True,
            charging_station_id=create_second_station.id
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.update_connector(db_session, create_connector.id, data)

        assert exc_info.value.status_code == 400
        assert "This charging station already has a connector with priority." in exc_info.value.detail

    def test_update_connector_count_constraint(
            self,
            db_session,
            create_connector,
            create_second_station,
            create_second_connector,
            create_third_connector
    ):
        data = schemas.ConnectorCreate(
            name="Test Connector",
            priority=True,
            charging_station_id=create_second_station.id
        )

        with pytest.raises(HTTPException) as exc_info:
            crud.update_connector(db_session, create_connector.id, data)

        assert exc_info.value.status_code == 400
        assert "The number of connectors cannot exceed" in exc_info.value.detail

    def test_delete_connector_success(self, db_session, create_connector):
        crud.delete_connector(db_session, create_connector.id)

        connector_list = crud.get_connector_list(
            db=db_session,
            priority=None,
            charging_station_id=None,
            skip=None,
            limit=None
        )

        assert len(connector_list) == 0

    def test_delete_connector_wrong_id(self, db_session, create_connector):
        with pytest.raises(HTTPException) as exc_info:
            crud.delete_connector(db_session, "a73ee835-1201-4888-9d3a-911f48958b42")

        assert exc_info.value.status_code == 404
        assert "Connector instance not found." in exc_info.value.detail


class TestUserCrud:
    def test_create_user_success(self, db_session):
        data = schemas.UserCreate(username="admin", password="admin")

        user = crud.create_user(db_session, data)

        assert user.username == "admin"
        assert user.hashed_password != "admin"

    def test_create_user_not_unique(self, db_session, create_user):
        data = schemas.UserCreate(username="admin", password="admin")

        with pytest.raises(HTTPException) as exc_info:
            crud.create_user(db_session, data)

        assert exc_info.value.status_code == 400
        assert "is already registered." in exc_info.value.detail

    def test_update_user_success(self, db_session, create_user):
        data = schemas.UserCreate(username="admin update", password="admin")

        user = crud.update_user(db_session, create_user.username, data)

        assert user.username == "admin update"
        assert user.hashed_password != "admin"

    def test_update_user_wrong_username(self, db_session):
        data = schemas.UserCreate(username="admin update", password="admin")

        with pytest.raises(HTTPException) as exc_info:
            crud.update_user(db_session, "Puszek", data)

        assert exc_info.value.status_code == 404
        assert "not found." in exc_info.value.detail

    def test_update_user_not_unique(self, db_session, create_user, create_second_user):
        data = schemas.UserCreate(username="admin2", password="admin")

        with pytest.raises(HTTPException) as exc_info:
            crud.update_user(db_session, create_user.username, data)

        assert exc_info.value.status_code == 400
        assert "violates the database's integrity" in exc_info.value.detail

    def test_delete_user_success(self, db_session, create_user):
        crud.delete_user(db_session, create_user.username)

        query = db_session.query(User).all()

        assert len(query) == 0

    def test_delete_user_wrong_username(self, db_session):
        with pytest.raises(HTTPException) as exc_info:
            crud.delete_user(db_session, "Puszek")

        assert exc_info.value.status_code == 404
        assert "not found." in exc_info.value.detail
