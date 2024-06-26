from pydantic import BaseModel, UUID4, Field, conint, confloat, field_validator, ConfigDict
from typing import List, Optional
from uuid import uuid4
from ipaddress import IPv4Address, IPv6Address
from ..models.models import CurrentTypeEnum


class ChargingStationIDOnly(BaseModel):
    id: UUID4


class ChargingStationTypeBase(BaseModel):
    name: str
    plug_count: conint(gt=0)
    efficiency: confloat(ge=0, le=100)
    current_type: CurrentTypeEnum


class ChargingStationTypeCreate(ChargingStationTypeBase):
    pass


class ChargingStationTypeNoList(ChargingStationTypeBase):
    id: UUID4


class ChargingStationType(ChargingStationTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    charging_stations: List[ChargingStationIDOnly] = []


class ConnectorBase(BaseModel):
    name: str
    priority: bool


class ConnectorCreate(ConnectorBase):
    charging_station_id: Optional[UUID4] = None


class ConnectorCreateWithStation(ConnectorBase):
    pass


class Connector(ConnectorBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    charging_station_id: Optional[UUID4] = None


class ChargingStationBase(BaseModel):
    name: str
    device_id: Optional[UUID4] = Field(default_factory=uuid4)
    ip_address: str
    firmware_version: str

    @field_validator("ip_address")
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
    type_id: UUID4
    connectors: List[ConnectorCreateWithStation]


class ChargingStation(ChargingStationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    type: ChargingStationTypeNoList
    connectors: List[Connector] = []


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
