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
