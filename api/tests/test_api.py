from ..main import app
from ..utils.auth import get_current_user
from ..schemas import schemas


class TestChargingStationType:
    def test_create_charging_station_type_success_ac(self, client):
        test_data = {
            "name": "Test Station Type",
            "plug_count": 2,
            "efficiency": 80.1,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 201

    def test_create_charging_station_type_success_dc(self, client):
        test_data = {
            "name": "Test Station Type",
            "plug_count": 2,
            "efficiency": 80.1,
            "current_type": "DC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 201

    def test_create_charging_station_type_unauthorized(self, client):
        test_data = {
            "name": "Test Station Type",
            "plug_count": 2,
            "efficiency": 80.1,
            "current_type": "AC"
        }

        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_create_charging_station_type_wrong_name_type(self, client):
        test_data = {
            "name": 1,
            "plug_count": 2,
            "efficiency": 80.1,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_type_wrong_plug_count_type(self, client):
        test_data = {
            "name": "test",
            "plug_count": "test",
            "efficiency": 80.1,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_type_wrong_plug_count_less_than_0(self, client):
        test_data = {
            "name": "test",
            "plug_count": -1,
            "efficiency": 80.1,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_type_wrong_efficiency_type(self, client):
        test_data = {
            "name": "test",
            "plug_count": 2,
            "efficiency": "test",
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_type_wrong_efficiency_bigger_than_100(self, client):
        test_data = {
            "name": "test",
            "plug_count": 2,
            "efficiency": 100.01,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_type_wrong_efficiency_less_than_0(self, client):
        test_data = {
            "name": "test",
            "plug_count": 2,
            "efficiency": -0.01,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_type_wrong_current_type_not_enum(self, client):
        test_data = {
            "name": "test",
            "plug_count": 2,
            "efficiency": 1,
            "current_type": "test"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_type_wrong_current_type_wrong_type(self, client):
        test_data = {
            "name": "test",
            "plug_count": 2,
            "efficiency": 1,
            "current_type": 1
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_type_not_unique(self, client, create_station_type):
        test_data = {
            "name": "Test Station Type",
            "plug_count": 2,
            "efficiency": 1,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_station_types/", json=test_data)

        assert response.status_code == 400
        assert "violates the database's integrity" in response.json()["detail"]

    def test_read_charging_station_type_success(self, client, create_station_type, create_station):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get(f"/charging_station_types/{create_station_type.id}")

        assert response.status_code == 200
        assert response.json() == {
            "name": f"{create_station_type.name}",
            "plug_count": create_station_type.plug_count,
            "efficiency": create_station_type.efficiency,
            "current_type": "AC",
            "id": f"{create_station_type.id}",
            "charging_stations": [
                {"id": f"{create_station.id}"}
            ]
        }

    def test_read_charging_station_type_unauthorized(self, client, create_station_type):
        response = client.get(f"/charging_station_types/{create_station_type.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_read_charging_station_type_wrong_id(self, client, create_station_type):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_station_types/ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_read_charging_station_type_list_success(
            self,
            client,
            create_station_type,
            create_second_station_type,
            create_second_station
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_station_types/")

        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json() == [
            {
                "name": f"{create_station_type.name}",
                "plug_count": create_station_type.plug_count,
                "efficiency": create_station_type.efficiency,
                "current_type": "AC",
                "id": f"{create_station_type.id}",
                "charging_stations": []
            },
            {
                "name": f"{create_second_station_type.name}",
                "plug_count": create_second_station_type.plug_count,
                "efficiency": create_second_station_type.efficiency,
                "current_type": "DC",
                "id": f"{create_second_station_type.id}",
                "charging_stations": [
                    {"id": f"{create_second_station.id}"}
                ]
            }
        ]

    def test_read_charging_station_type_list_success_query_plug(
            self,
            client,
            create_station_type,
            create_second_station_type
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_station_types/?plug_count=1")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_charging_station_type_list_success_query_min_eff(
            self,
            client,
            create_station_type,
            create_second_station_type
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_station_types/?min_efficiency=90")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_charging_station_type_list_success_query_max_eff(
            self,
            client,
            create_station_type,
            create_second_station_type
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_station_types/?max_efficiency=40")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_charging_station_type_list_success_query_current(
            self,
            client,
            create_station_type,
            create_second_station_type
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_station_types/?current_type=AC")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_charging_station_type_list_success_query_skip(
            self,
            client,
            create_station_type,
            create_second_station_type
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_station_types/?skip=2")

        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_read_charging_station_type_list_success_query_limit(
            self,
            client,
            create_station_type,
            create_second_station_type
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_station_types/?limit=1")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_charging_station_type_list_success_empty(self, client):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_station_types/")

        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_read_charging_station_type_list_unauthorized(self, client):
        response = client.get("/charging_station_types/")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_update_charging_station_type_success_ac(self, client, create_station_type):
        test_data = {
            "name": "Test Station Type Updated",
            "plug_count": 2,
            "efficiency": 80.1,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 200

    def test_update_charging_station_type_success_dc(self, client, create_station_type):
        test_data = {
            "name": "Test Station Type Updated",
            "plug_count": 2,
            "efficiency": 80.1,
            "current_type": "DC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 200

    def test_update_charging_station_type_wrong_id(self, client, create_station_type):
        test_data = {
            "name": "Test Station Type Updated",
            "plug_count": 2,
            "efficiency": 80.1,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put("/charging_station_types/ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3", json=test_data)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_charging_station_type_wrong_name_type(self, client, create_station_type):
        test_data = {
            "name": 2,
            "plug_count": 2,
            "efficiency": 80.1,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_type_wrong_plug_type(self, client, create_station_type):
        test_data = {
            "name": "test",
            "plug_count": "test",
            "efficiency": 80.1,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_type_wrong_plug_count_negative(self, client, create_station_type):
        test_data = {
            "name": "test",
            "plug_count": -1,
            "efficiency": 80.1,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_type_wrong_efficiency_type(self, client, create_station_type):
        test_data = {
            "name": "test",
            "plug_count": 1,
            "efficiency": "test",
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_type_wrong_efficiency_below_0(self, client, create_station_type):
        test_data = {
            "name": "test",
            "plug_count": 1,
            "efficiency": -2,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_type_wrong_efficiency_too_high(self, client, create_station_type):
        test_data = {
            "name": "test",
            "plug_count": 1,
            "efficiency": 101,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_type_wrong_current_type(self, client, create_station_type):
        test_data = {
            "name": "test",
            "plug_count": 1,
            "efficiency": 91,
            "current_type": 2
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_type_wrong_current_not_enum(self, client, create_station_type):
        test_data = {
            "name": "test",
            "plug_count": 1,
            "efficiency": 91,
            "current_type": "test"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_type_not_unique(self, client, create_station_type, create_second_station_type):
        test_data = {
            "name": "Test Station Type 2",
            "plug_count": 1,
            "efficiency": 91,
            "current_type": "AC"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 400
        assert "violates the database's integrity" in response.json()["detail"]

    def test_update_charging_station_type_unauthorized(self, client, create_station_type):
        test_data = {
            "name": "Test Station Type Updated",
            "plug_count": 2,
            "efficiency": 80.1,
            "current_type": "AC"
        }

        response = client.put(f"/charging_station_types/{create_station_type.id}", json=test_data)

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_delete_charging_station_type_success(self, client, create_station_type):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.delete(f"/charging_station_types/{create_station_type.id}")

        assert response.status_code == 204

    def test_delete_charging_station_type_wrong_id(self, client, create_station_type):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.delete("/charging_station_types/ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_delete_charging_station_type_assigned(self, client, create_station_type, create_station):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.delete(f"/charging_station_types/{create_station_type.id}")

        assert response.status_code == 400
        assert "Make sure that no Charging Stations are assigned to this Type." in response.json()["detail"]

    def test_delete_charging_station_type_unauthorized(self, client, create_station_type):
        response = client.delete(f"/charging_station_types/{create_station_type.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]


class TestChargingStation:
    def test_create_charging_station_success(self, client, create_station_type):
        test_data = {
            "name": "Test Station",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 201

    def test_create_charging_station_wrong_name_type(self, client, create_station_type):
        test_data = {
            "name": 2,
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_name_not_unique(self, client, create_station_type, create_station):
        test_data = {
            "name": "Test Station",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_create_charging_station_wrong_device_id_type(self, client, create_station_type):
        test_data = {
            "name": "station",
            "device_id": 1,
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_device_id_not_unique(self, client, create_station_type, create_station):
        test_data = {
            "name": "Test",
            "device_id": f"urn:uuid:{create_station.device_id}",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_create_charging_station_wrong_ip_type(self, client, create_station_type):
        test_data = {
            "name": "test",
            "ip_address": 2,
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_wrong_ip_invalid(self, client, create_station_type):
        test_data = {
            "name": "test",
            "ip_address": "256.0.0.1",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_ip_not_unique(self, client, create_station_type, create_station):
        test_data = {
            "name": "Test Station",
            "ip_address": "179.148.235.118",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_create_charging_station_wrong_firmware_type(self, client, create_station_type):
        test_data = {
            "name": "test",
            "ip_address": "192.168.1.2",
            "firmware_version": 1,
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_wrong_type_id_type(self, client, create_station_type):
        test_data = {
            "name": "test",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1",
            "type_id": 1,
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_wrong_type_id(self, client, create_station_type):
        test_data = {
            "name": "test",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1",
            "type_id": "urn:uuid:ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_create_charging_station_connector_name_wrong_type(self, client, create_station_type):
        test_data = {
            "name": "Test Station",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": 1,
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_connector_name_not_unique(self, client, create_station_type, create_connector):
        test_data = {
            "name": "Test Station",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_create_charging_station_connector_wrong_priority_type(self, client, create_station_type):
        test_data = {
            "name": "Test Station",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": "test"
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 422

    def test_create_charging_station_connector_wrong_connector_count(self, client, create_station_type):
        test_data = {
            "name": "Test Station",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": False
                },
                {
                    "name": "Test Connector 2",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 400
        assert "The number of connectors" in response.json()["detail"]

    def test_create_charging_station_connector_wrong_connector_priority(self, client, create_second_station_type):
        test_data = {
            "name": "Test Station",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_second_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                },
                {
                    "name": "Test Connector 2",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 400
        assert "Only one connector in each Charging Station can have priority." in response.json()["detail"]

    def test_create_charging_station_unauthorized(self, client, create_station_type):
        test_data = {
            "name": "Unauthorized Station",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        response = client.post("/charging_stations/", json=test_data)

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_read_charging_station_success(self, client, create_station, create_station_type, create_connector):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get(f"/charging_stations/{create_station.id}")

        assert response.status_code == 200
        assert response.json() == {
            "name": f"{create_station.name}",
            "device_id": f"{create_station.device_id}",
            "ip_address": f"{create_station.ip_address}",
            "firmware_version": f"{create_station.firmware_version}",
            "id": f"{create_station.id}",
            "type": {
                "name": f"{create_station_type.name}",
                "plug_count": create_station_type.plug_count,
                "efficiency": create_station_type.efficiency,
                "current_type": "AC",
                "id": f"{create_station_type.id}"
            },
            "connectors": [
                {
                    "charging_station_id": f"{create_connector.charging_station_id}",
                    "id": f"{create_connector.id}",
                    "name": f"{create_connector.name}",
                    "priority": create_connector.priority
                }
            ]
        }

    def test_read_charging_station_wrong_id(self, client, create_station, create_connector):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_read_charging_station_wrong_connector_count(self, client, create_station):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get(f"/charging_stations/{create_station.id}")

        assert response.status_code == 400
        assert "connectors instead of" in response.json()["detail"]

    def test_read_charging_station_unauthorized(self, client, create_station, create_connector):
        response = client.get(f"/charging_stations/{create_station.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_read_charging_station_list_success_empty(self, client):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/")

        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_read_charging_station_list_success(
            self,
            client,
            create_station_type,
            create_second_station_type,
            create_station,
            create_connector,
            create_second_station,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/")

        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json() == [
            {
                "name": f"{create_station.name}",
                "device_id": f"{create_station.device_id}",
                "ip_address": f"{create_station.ip_address}",
                "firmware_version": f"{create_station.firmware_version}",
                "id": f"{create_station.id}",
                "type": {
                    "name": f"{create_station_type.name}",
                    "plug_count": create_station_type.plug_count,
                    "efficiency": create_station_type.efficiency,
                    "current_type": "AC",
                    "id": f"{create_station_type.id}"
                },
                "connectors": [
                    {
                        "charging_station_id": f"{create_connector.charging_station_id}",
                        "id": f"{create_connector.id}",
                        "name": f"{create_connector.name}",
                        "priority": create_connector.priority
                    }
                ]
            },
            {
                "name": f"{create_second_station.name}",
                "device_id": f"{create_second_station.device_id}",
                "ip_address": f"{create_second_station.ip_address}",
                "firmware_version": f"{create_second_station.firmware_version}",
                "id": f"{create_second_station.id}",
                "type": {
                    "name": f"{create_second_station_type.name}",
                    "plug_count": create_second_station_type.plug_count,
                    "efficiency": create_second_station_type.efficiency,
                    "current_type": "DC",
                    "id": f"{create_second_station_type.id}"
                },
                "connectors": [
                    {
                        "charging_station_id": f"{create_second_connector.charging_station_id}",
                        "id": f"{create_second_connector.id}",
                        "name": f"{create_second_connector.name}",
                        "priority": create_second_connector.priority
                    },
                    {
                        "charging_station_id": f"{create_third_connector.charging_station_id}",
                        "id": f"{create_third_connector.id}",
                        "name": f"{create_third_connector.name}",
                        "priority": create_third_connector.priority
                    }
                ]
            }
        ]

    def test_read_charging_station_list_success_query_plug(
            self,
            client,
            create_station,
            create_connector,
            create_second_station,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/?plug_count=1")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_charging_station_list_success_query_min_eff(
            self,
            client,
            create_station,
            create_connector,
            create_second_station,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/?min_efficiency=90")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_charging_station_list_success_query_max_eff(
            self,
            client,
            create_station,
            create_connector,
            create_second_station,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/?max_efficiency=60")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_charging_station_list_success_query_current(
            self,
            client,
            create_station,
            create_connector,
            create_second_station,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/?current_type=AC")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_charging_station_list_success_query_firmware(
            self,
            client,
            create_station,
            create_connector,
            create_second_station,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/?firmware_version=idklol")

        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_read_charging_station_list_success_query_skip(
            self,
            client,
            create_station,
            create_connector,
            create_second_station,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/?skip=1")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_charging_station_list_success_query_limit(
            self,
            client,
            create_station,
            create_connector,
            create_second_station,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/?limit=1")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_charging_station_list_wrong_connector_count(self, client, create_station):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/")

        assert response.status_code == 400
        assert "connectors instead of" in response.json()["detail"]

    def test_read_charging_station_list_unauthorized(self, client):
        response = client.get("/charging_stations/")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_update_charging_station_success(self, client, create_station_type, create_station):
        test_data = {
            "name": "Test Station Update",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 200

    def test_update_charging_station_wrong_id(self, client, create_station_type, create_station):
        test_data = {
            "name": "Test Station Update",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put("/charging_stations/ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3", json=test_data)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_charging_station_wrong_name_type(self, client, create_station_type, create_station):
        test_data = {
            "name": 1,
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_wrong_name_not_unique(
            self,
            client,
            create_station_type,
            create_station,
            create_second_station
    ):
        test_data = {
            "name": "Test Station 2",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_update_charging_station_wrong_device_id_type(self, client, create_station_type, create_station):
        test_data = {
            "name": "test",
            "device_id": 1,
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_wrong_device_id_not_unique(
            self,
            client,
            create_station_type,
            create_station,
            create_second_station
    ):
        test_data = {
            "name": "Test Station",
            "device_id": f"urn:uuid:{create_second_station.device_id}",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_update_charging_station_wrong_ip_type(self, client, create_station_type, create_station):
        test_data = {
            "name": "test",
            "ip_address": 1,
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_wrong_ip_invalid(self, client, create_station_type, create_station):
        test_data = {
            "name": "test",
            "ip_address": "256.0.0.1",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_wrong_ip_not_unique(
            self,
            client,
            create_station_type,
            create_station,
            create_second_station
    ):
        test_data = {
            "name": "test",
            "ip_address": "53.72.164.8",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_update_charging_station_wrong_firmware_type(self, client, create_station_type, create_station):
        test_data = {
            "name": "test",
            "ip_address": "192.168.1.2",
            "firmware_version": 1,
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_wrong_type_id_type(self, client, create_station_type, create_station):
        test_data = {
            "name": "test",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1",
            "type_id": 1,
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_wrong_type_id(self, client, create_station_type, create_station):
        test_data = {
            "name": "test",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1",
            "type_id": "urn:uuid:ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_charging_station_wrong_connector_name_type(self, client, create_station_type, create_station):
        test_data = {
            "name": "test",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": 1,
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 422

    def test_update_charging_station_wrong_connector_name_not_unique(
            self,
            client,
            create_station_type,
            create_station,
            create_third_connector
    ):
        test_data = {
            "name": "test",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector 3",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_update_charging_station_wrong_connector_count(self, client, create_station_type, create_station):
        test_data = {
            "name": "test",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector 3",
                    "priority": True
                },
                {
                    "name": "Test Connector",
                    "priority": False
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 400
        assert "The number of connectors must equal" in response.json()["detail"]

    def test_update_charging_station_wrong_connector_priority(self, client, create_second_station_type, create_station):
        test_data = {
            "name": "test",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1",
            "type_id": f"urn:uuid:{create_second_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector 3",
                    "priority": True
                },
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 400
        assert "Only one connector in each Charging Station can have priority." in response.json()["detail"]

    def test_update_charging_station_unauthorized(self, client, create_station_type, create_station):
        test_data = {
            "name": "Test Station Update",
            "ip_address": "192.168.1.2",
            "firmware_version": "v1.2.4",
            "type_id": f"urn:uuid:{create_station_type.id}",
            "connectors": [
                {
                    "name": "Test Connector",
                    "priority": True
                }
            ]
        }

        response = client.put(f"/charging_stations/{create_station.id}", json=test_data)

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_delete_charging_station_success(self, client, create_station):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.delete(f"/charging_stations/{create_station.id}")

        assert response.status_code == 204

    def test_delete_charging_station_wrong_id(self, client, create_station):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.delete("/charging_stations/ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_delete_charging_station_unauthorized(self, client, create_station):
        response = client.delete(f"/charging_stations/{create_station.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]


class TestConnector:
    def test_create_connector_success_no_charging_station(self, client):
        test_data = {
            "name": "Test Connector",
            "priority": True
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/connectors/", json=test_data)

        assert response.status_code == 201

    def test_create_connector_success(self, client, create_station):
        test_data = {
            "name": "Test Connector",
            "priority": True,
            "charging_station_id": f"urn:uuid:{create_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/connectors/", json=test_data)

        assert response.status_code == 201

    def test_create_connector_wrong_name_type(self, client, create_station):
        test_data = {
            "name": 1,
            "priority": True,
            "charging_station_id": f"urn:uuid:{create_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/connectors/", json=test_data)

        assert response.status_code == 422

    def test_create_connector_wrong_name_not_unique(self, client, create_station, create_second_connector):
        test_data = {
            "name": "Test Connector 2",
            "priority": True,
            "charging_station_id": f"urn:uuid:{create_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/connectors/", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_create_connector_wrong_priority_type(self, client, create_station):
        test_data = {
            "name": "Test Connector",
            "priority": "test",
            "charging_station_id": f"urn:uuid:{create_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/connectors/", json=test_data)

        assert response.status_code == 422

    def test_create_connector_wrong_charging_station_id(self, client, create_station):
        test_data = {
            "name": "Test Connector",
            "priority": True,
            "charging_station_id": "urn:uuid:ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/connectors/", json=test_data)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_create_connector_count_constraint(self, client, create_station, create_connector):
        test_data = {
            "name": "Test",
            "priority": False,
            "charging_station_id": f"urn:uuid:{create_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/connectors/", json=test_data)

        assert response.status_code == 400
        assert "The number of connectors cannot exceed" in response.json()["detail"]

    def test_create_connector_priority_constraint(self, client, create_second_station, create_third_connector):
        test_data = {
            "name": "Test",
            "priority": True,
            "charging_station_id": f"urn:uuid:{create_second_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.post("/connectors/", json=test_data)

        assert response.status_code == 400
        assert "This charging station already has a connector with priority." in response.json()["detail"]

    def test_create_connector_unauthorized(self, client):
        test_data = {
            "name": "Test Connector",
            "priority": True
        }

        response = client.post("/connectors/", json=test_data)

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_read_connector_success(self, client, create_connector):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get(f"/connectors/{create_connector.id}")

        assert response.status_code == 200
        assert response.json() == {
            "name": f"{create_connector.name}",
            "priority": create_connector.priority,
            "id": f"{create_connector.id}",
            "charging_station_id": f"{create_connector.charging_station_id}"
        }

    def test_read_connector_wrong_id(self, client, create_connector):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/connectors/ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_read_connector_unauthorized(self, client, create_connector):
        response = client.get(f"/connectors/{create_connector.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_read_connector_list_success_empty(self, client):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/connectors/")

        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_read_connector_list_success(
            self,
            client,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/connectors/")

        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json() == [
            {
                "name": f"{create_connector.name}",
                "priority": create_connector.priority,
                "id": f"{create_connector.id}",
                "charging_station_id": f"{create_connector.charging_station_id}"
            },
            {
                "name": f"{create_second_connector.name}",
                "priority": create_second_connector.priority,
                "id": f"{create_second_connector.id}",
                "charging_station_id": f"{create_second_connector.charging_station_id}"
            },
            {
                "name": f"{create_third_connector.name}",
                "priority": create_third_connector.priority,
                "id": f"{create_third_connector.id}",
                "charging_station_id": f"{create_third_connector.charging_station_id}"
            }
        ]

    def test_read_connector_list_success_query_priority(
            self,
            client,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/connectors/?priority=True")

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_read_connector_list_success_query_charging_station_id(
            self,
            client,
            create_station,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get(f"/connectors/?charging_station_id={create_station.id}")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_connector_list_success_query_skip(
            self,
            client,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/connectors/?skip=2")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_connector_list_success_query_limit(
            self,
            client,
            create_connector,
            create_second_connector,
            create_third_connector
    ):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/connectors/?limit=2")

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_read_connector_list_unauthorized(self, client):
        response = client.get("/connectors/")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_update_connector_success_no_station(self, client, create_connector):
        test_data = {
            "name": "Test Connector",
            "priority": True
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/connectors/{create_connector.id}", json=test_data)

        assert response.status_code == 200

    def test_update_connector_success(self, client, create_connector, create_station):
        test_data = {
            "name": "Test Connector",
            "priority": True,
            "charging_station_id": f"urn:uuid:{create_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/connectors/{create_connector.id}", json=test_data)

        assert response.status_code == 200

    def test_update_connector_wrong_id(self, client, create_connector, create_station):
        test_data = {
            "name": "Test Connector",
            "priority": True,
            "charging_station_id": f"urn:uuid:{create_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put("/connectors/ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3", json=test_data)

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_connector_wrong_name_type(self, client, create_connector, create_station):
        test_data = {
            "name": 1,
            "priority": True,
            "charging_station_id": f"urn:uuid:{create_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/connectors/{create_connector.id}", json=test_data)

        assert response.status_code == 422

    def test_update_connector_wrong_name_not_unique(
            self,
            client,
            create_connector,
            create_station,
            create_second_connector
    ):
        test_data = {
            "name": "Test Connector 2",
            "priority": True,
            "charging_station_id": f"urn:uuid:{create_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/connectors/{create_connector.id}", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_update_connector_wrong_priority_type(self, client, create_connector, create_station):
        test_data = {
            "name": "test",
            "priority": "test",
            "charging_station_id": f"urn:uuid:{create_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/connectors/{create_connector.id}", json=test_data)

        assert response.status_code == 422

    def test_update_connector_wrong_charging_station_id_type(self, client, create_connector, create_station):
        test_data = {
            "name": "test",
            "priority": True,
            "charging_station_id": 1
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/connectors/{create_connector.id}", json=test_data)

        assert response.status_code == 422

    def test_update_connector_wrong_charging_station_id(self, client, create_connector, create_station):
        test_data = {
            "name": "testt",
            "priority": True,
            "charging_station_id": f"urn:uuid:{create_connector.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/connectors/{create_connector.id}", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_update_connector_count_constraint(
            self,
            client,
            create_connector,
            create_second_connector,
            create_third_connector,
            create_second_station
    ):
        test_data = {
            "name": "test",
            "priority": False,
            "charging_station_id": f"urn:uuid:{create_second_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/connectors/{create_connector.id}", json=test_data)

        assert response.status_code == 400
        assert "The number of connectors cannot exceed" in response.json()["detail"]

    def test_update_connector_priority_constraint(
            self,
            client,
            create_connector,
            create_third_connector,
            create_second_station
    ):
        test_data = {
            "name": "test",
            "priority": True,
            "charging_station_id": f"urn:uuid:{create_second_station.id}"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/connectors/{create_connector.id}", json=test_data)

        assert response.status_code == 400
        assert "This charging station already has a connector with priority." in response.json()["detail"]

    def test_update_connector_unauthorized(self, client, create_connector):
        test_data = {
            "name": "Test Connector",
            "priority": True
        }

        response = client.put(f"/connectors/{create_connector.id}", json=test_data)

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_delete_connector_success(self, client, create_connector):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.delete(f"/connectors/{create_connector.id}")

        assert response.status_code == 204

    def test_delete_connector_wrong_id(self, client, create_connector):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.delete("/connectors/ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_delete_connector_unauthorized(self, client, create_connector):
        response = client.delete(f"/connectors/{create_connector.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]


class TestUser:
    def test_create_user_success(self, client):
        test_data = {
            "username": "Test User",
            "password": "SuperSafePassword"
        }

        response = client.post("/users/", json=test_data)

        assert response.status_code == 201
        assert response.json() == {"username": "Test User"}

    def test_create_user_wrong_username_type(self, client):
        test_data = {
            "username": 1,
            "password": "SuperSafePassword"
        }

        response = client.post("/users/", json=test_data)

        assert response.status_code == 422

    def test_create_user_wrong_username_not_unique(self, client, create_user):
        test_data = {
            "username": "admin",
            "password": "SuperSafePassword"
        }

        response = client.post("/users/", json=test_data)

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_create_user_wrong_password_type(self, client):
        test_data = {
            "username": "user",
            "password": 1
        }

        response = client.post("/users/", json=test_data)

        assert response.status_code == 422

    def test_update_user_success(self, client, create_user):
        test_data = {
            "username": "TestUser",
            "password": "SuperSafePassword"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id=create_user.id,
            username=create_user.username
        )
        response = client.put(f"/users/{create_user.username}", json=test_data)

        assert response.status_code == 200
        assert response.json() == {"username": "TestUser"}

    def test_update_user_wrong_username_type(self, client, create_user):
        test_data = {
            "username": 1,
            "password": "SuperSafePassword"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id=create_user.id,
            username=create_user.username
        )
        response = client.put(f"/users/{create_user.username}", json=test_data)

        assert response.status_code == 422

    def test_update_user_wrong_username_not_unique(self, client, create_user, create_second_user):
        test_data = {
            "username": "admin2",
            "password": "SuperSafePassword"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id=create_user.id,
            username=create_user.username
        )
        response = client.put(f"/users/{create_user.username}", json=test_data)

        assert response.status_code == 400
        assert "integrity" in response.json()["detail"]

    def test_update_user_wrong_password_type(self, client, create_user):
        test_data = {
            "username": "admin",
            "password": 1
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id=create_user.id,
            username=create_user.username
        )
        response = client.put(f"/users/{create_user.username}", json=test_data)

        assert response.status_code == 422

    def test_update_user_unauthorized_not_logged_in(self, client, create_user):
        test_data = {
            "username": "TestUser",
            "password": "SuperSafePassword"
        }

        response = client.put(f"/users/{create_user.username}", json=test_data)

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_update_user_unauthorized_wrong_user(self, client, create_user):
        test_data = {
            "username": "TestUser",
            "password": "SuperSafePassword"
        }

        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.put(f"/users/{create_user.username}", json=test_data)

        assert response.status_code == 403
        assert "Cannot update other user's credentials." in response.json()["detail"]

    def test_delete_user_success(self, client, create_user):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id=create_user.id,
            username=create_user.username
        )
        response = client.delete(f"/users/{create_user.username}")

        assert response.status_code == 204

    def test_delete_user_unauthorized_not_logged_in(self, client, create_user):
        response = client.delete(f"/users/{create_user.username}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_delete_user_unauthorized_wrong_user(self, client, create_user):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.delete(f"/users/{create_user.username}")

        assert response.status_code == 403
        assert "Cannot delete other user's credentials." in response.json()["detail"]
