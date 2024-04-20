from ..main import app
from ..utils.auth import get_current_user
from ..schemas import schemas


class TestChargingStationTypeRouter:
    def test_create_charging_station_type_success(self, client):
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

    def test_read_charging_station_type_success(self, client, create_station_type):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get(f"/charging_station_types/{create_station_type.id}")

        assert response.status_code == 200

    def test_read_charging_station_type_unauthorized(self, client, create_station_type):
        response = client.get(f"/charging_station_types/{create_station_type.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_read_charging_station_type_list_success(self, client):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_station_types/")

        assert response.status_code == 200

    def test_read_charging_station_type_list_unauthorized(self, client):
        response = client.get("/charging_station_types/")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_update_charging_station_type_success(self, client, create_station_type):
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

    def test_delete_charging_station_type_unauthorized(self, client, create_station_type):
        response = client.delete(f"/charging_station_types/{create_station_type.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]


class TestChargingStationRouter:
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

    def test_read_charging_station_success(self, client, create_station, create_connector):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get(f"/charging_stations/{create_station.id}")

        assert response.status_code == 200

    def test_read_charging_station_unauthorized(self, client, create_station, create_connector):
        response = client.get(f"/charging_stations/{create_station.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_read_charging_station_list_success(self, client):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/charging_stations/")

        assert response.status_code == 200

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

    def test_delete_charging_station_unauthorized(self, client, create_station):
        response = client.delete(f"/charging_stations/{create_station.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]


class TestConnectorRouter:
    def test_create_connector_success(self, client):
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

    def test_read_connector_unauthorized(self, client, create_connector):
        response = client.get(f"/connectors/{create_connector.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_read_connector_list_success(self, client):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.get("/connectors/")

        assert response.status_code == 200

    def test_read_connector_list_unauthorized(self, client):
        response = client.get("/connectors/")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_update_connector_success(self, client, create_connector):
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

    def test_update_connector_unauthorized(self, client, create_connector):
        test_data = {
            "name": "Test Connector",
            "priority": True
        }

        response = client.put(f"/connectors/{create_connector.id}", json=test_data)

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_delete_connector_type_success(self, client, create_connector):
        app.dependency_overrides[get_current_user] = lambda: schemas.User(
            id="ac1fdd79-5f47-4ec1-8ab4-ea8daf7a45d3",
            username="new_user"
        )
        response = client.delete(f"/connectors/{create_connector.id}")

        assert response.status_code == 204

    def test_delete_connector_unauthorized(self, client, create_connector):
        response = client.delete(f"/connectors/{create_connector.id}")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]


class TestUserRouter:
    def test_create_user_success(self, client):
        test_data = {
            "username": "Test User",
            "password": "SuperSafePassword"
        }

        response = client.post("/users/", json=test_data)

        assert response.status_code == 201

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
