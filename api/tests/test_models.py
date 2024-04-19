from ..models import models


class TestChargingStationTypeModel:
    def test_create_and_fetch_charging_station_type(self, db_session, create_station_type):
        fetched = db_session.query(models.ChargingStationType).filter_by(name=create_station_type.name).first()

        assert fetched is not None
        assert fetched.efficiency == create_station_type.efficiency

    def test_update_charging_station_type(self, db_session, create_station_type):
        fetched = db_session.query(models.ChargingStationType).filter_by(name=create_station_type.name).first()
        fetched.efficiency = 95.2

        assert fetched.efficiency == 95.2

    def test_delete_charging_station_type(self, db_session, create_station_type):
        fetched = db_session.query(models.ChargingStationType).filter_by(name=create_station_type.name).first()
        db_session.delete(fetched)
        db_session.commit()

        assert db_session.query(models.ChargingStationType).filter_by(name=create_station_type.name).count() == 0


class TestChargingStationModel:
    def test_create_and_fetch_charging_station(self, db_session, create_station):
        fetched = db_session.query(models.ChargingStation).filter_by(name=create_station.name).first()

        assert fetched is not None
        assert fetched.device_id == create_station.device_id

    def test_update_charging_station(self, db_session, create_station):
        fetched = db_session.query(models.ChargingStation).filter_by(name=create_station.name).first()
        fetched.name = "Another station name"

        assert fetched.name == "Another station name"

    def test_delete_charging_station(self, db_session, create_station):
        fetched = db_session.query(models.ChargingStation).filter_by(name=create_station.name).first()
        db_session.delete(fetched)
        db_session.commit()

        assert db_session.query(models.ChargingStation).filter_by(name=create_station.name).count() == 0


class TestConnectorModel:
    def test_create_and_fetch_connector(self, db_session, create_connector):
        fetched = db_session.query(models.Connector).filter_by(name=create_connector.name).first()

        assert fetched is not None
        assert fetched.priority == create_connector.priority

    def test_update_connector(self, db_session, create_connector):
        fetched = db_session.query(models.Connector).filter_by(name=create_connector.name).first()
        fetched.priority = False

        assert fetched.priority is False

    def test_delete_connector(self, db_session, create_connector):
        fetched = db_session.query(models.Connector).filter_by(name=create_connector.name).first()
        db_session.delete(fetched)
        db_session.commit()

        assert db_session.query(models.Connector).filter_by(name=create_connector.name).count() == 0


class TestUserModel:
    def test_create_and_fetch_user(self, db_session, create_user):
        fetched = db_session.query(models.User).filter_by(username=create_user.username).first()

        assert fetched is not None
        assert fetched.username == create_user.username

    def test_update_user(self, db_session, create_user):
        fetched = db_session.query(models.User).filter_by(username=create_user.username).first()
        fetched.username = "Puszek"

        assert fetched.username == "Puszek"

    def test_delete_user(self, db_session, create_user):
        fetched = db_session.query(models.User).filter_by(username=create_user.username).first()
        db_session.delete(fetched)
        db_session.commit()

        assert db_session.query(models.User).filter_by(username=create_user.username).count() == 0


class TestModelsRelationships:
    def test_relationships_charging_station_type(self, db_session, create_station_type, create_station):
        fetched = db_session.query(models.ChargingStationType).filter_by(name=create_station_type.name).first()

        assert len(fetched.charging_stations) == 1

    def test_relationships_charging_station(
            self,
            db_session,
            create_station_type,
            create_station,
            create_connector
    ):
        fetched = db_session.query(models.ChargingStation).filter_by(name=create_station.name).first()

        assert fetched.type.plug_count == create_station_type.plug_count
        assert len(fetched.connectors) == 1

    def test_relationships_connector(self, db_session, create_station, create_connector):
        fetched = db_session.query(models.Connector).filter_by(name=create_connector.name).first()

        assert fetched.charging_station.name == create_station.name
