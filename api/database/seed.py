from ..models.models import ChargingStationType
import logging

logger = logging.getLogger(__name__)


default_charging_station_types = [
    {'name': 'Type A', 'plug_count': 2, 'efficiency': 88.53, 'current_type': 'AC'},
    {'name': 'Type B', 'plug_count': 2, 'efficiency': 87.57, 'current_type': 'DC'},
    {'name': 'Type C', 'plug_count': 1, 'efficiency': 93.06, 'current_type': 'AC'},
    {'name': 'Type D', 'plug_count': 3, 'efficiency': 83.14, 'current_type': 'DC'},
    {'name': 'Type E', 'plug_count': 1, 'efficiency': 87.82, 'current_type': 'AC'}
]


def seed_charging_station_types(db_session):
    existing_types = db_session.query(ChargingStationType).count()
    if existing_types == 0:
        types = [ChargingStationType(**data) for data in default_charging_station_types]
        db_session.add_all(types)
        db_session.commit()
        logger.info("Database has been seeded with initial charging station types.")
    else:
        logger.info("Charging station types already exist. No changes made.")
