import pytest
from pydantic import ValidationError
from ..schemas.schemas import ChargingStationBase


def test_valid_ipv4_address():
    station = ChargingStationBase(name="Station", device_id=None, ip_address="192.168.1.1", firmware_version="1.0")
    assert station.ip_address == "192.168.1.1"

def test_valid_ipv6_address():
    station = ChargingStationBase(name="Station", device_id=None, ip_address="2001:0db8:85a3:0000:0000:8a2e:0370:7334", firmware_version="1.0")
    assert station.ip_address == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"

def test_invalid_ip_address():
    with pytest.raises(ValidationError) as exc_info:
        ChargingStationBase(name="Station", device_id=None, ip_address="192.168.300.1", firmware_version="1.0")

    assert exc_info