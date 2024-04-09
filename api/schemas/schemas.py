from pydantic import BaseModel, UUID4, Field, conint, confloat, validator
from typing import List
from uuid import uuid4
from ipaddress import IPv4Address, IPv6Address
from ..models.models import CurrentTypeEnum


class ChargingStationTypeBase(BaseModel):
    name: str
    plug_count: conint(gt=0)
    efficiency: confloat(ge=0, le=100)
    current_type: CurrentTypeEnum


class ChargingStationTypeCreate(ChargingStationTypeBase):
    pass


class ChargingStationType(ChargingStationTypeBase):
    id: UUID4
    charging_stations: List[UUID4] = []

    class Config:
        orm_mode = True


class ConnectorBase(BaseModel):
    name: str
    priority: bool
    charging_station_id: UUID4


class ConnectorCreate(ConnectorBase):
    pass


class Connector(ConnectorBase):
    id: UUID4

    class Config:
        orm_mode = True


class ChargingStationBase(BaseModel):
    name: str
    device_id: UUID4 = Field(default_factory=uuid4)
    ip_address: str
    firmware_version: str
    type_id: UUID4

    @validator("ip_address")
    def validate_ip_address(cls, v):
        try:
            IPv4Address(v)
        except ValueError:
            try:
                IPv6Address(v)
            except ValueError:
                raise ValueError("Invalid IP address format")
        return v


class ChargingStationCreate(ChargingStationBase):
    connectors: List[ConnectorCreate]


class ChargingStation(ChargingStationBase):
    id: UUID4
    type: ChargingStationType
    connectors: List[Connector] = []

    class Config:
        orm_mode = True
