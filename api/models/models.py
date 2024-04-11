from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import relationship
import uuid
import enum
from ..database.database import Base


class CurrentTypeEnum(enum.Enum):
    AC = "AC"
    DC = "DC"


class ChargingStationType(Base):
    __tablename__ = "charging_station_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    plug_count = Column(Integer, nullable=False)
    efficiency = Column(Float, nullable=False)
    current_type = Column(Enum(CurrentTypeEnum), nullable=False)
    charging_stations = relationship("ChargingStation", back_populates="type")


class ChargingStation(Base):
    __tablename__ = "charging_stations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    device_id = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    ip_address = Column(INET, unique=True, nullable=False)
    firmware_version = Column(String, nullable=False)
    type_id = Column(UUID(as_uuid=True), ForeignKey("charging_station_types.id"), nullable=False)
    type = relationship("ChargingStationType", back_populates="charging_stations")
    connectors = relationship("Connector", back_populates="charging_station")


class Connector(Base):
    __tablename__ = "connectors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    priority = Column(Boolean, default=False, nullable=False)
    charging_station_id = Column(UUID(as_uuid=True), ForeignKey("charging_stations.id"))
    charging_station = relationship("ChargingStation", back_populates="connectors")
