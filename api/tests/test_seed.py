from ..database.seed import seed_charging_station_types
from ..models.models import ChargingStationType


class TestSeed:
    def test_seed_data_when_db_empty(self, db_session):
        assert db_session.query(ChargingStationType).count() == 0

        seed_charging_station_types(db_session)

        assert db_session.query(ChargingStationType).count() == 5

    def test_no_seed_data_when_db_not_empty(self, db_session):
        sample_type = ChargingStationType(name="Type F", plug_count=2, efficiency=1, current_type="DC")
        db_session.add(sample_type)
        db_session.commit()

        seed_charging_station_types(db_session)

        assert db_session.query(ChargingStationType).count() == 1