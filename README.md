<br />
<div align="center">
  <a href="https://github.com/jmroczkowski99/EVChargingStation">
    <img src="https://github.com/jmroczkowski99/EVChargingStation/assets/146372897/12a23e7d-04a8-4201-b876-ac2bf6272df9" alt="Logo" width="240" height="240">
  </a>

<h3 align="center">EVChargingStation</h3>

  <p align="center">
    Electric vehicle charging station management system API
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#authentication-and-authorization">Authentication and authorization</a></li>
        <li><a href="#users">Users</a></li>
        <li><a href="#charging-station-types">Charging Station Types</a></li>
        <li><a href="#charging-stations">Charging Stations</a></li>
        <li><a href="#connectors">Connectors</a></li>
        <li><a href="#logging">Logging</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
# About The Project

API for managing an electric vehicle charging station system. It supports creating, reading, updating, and deleting information about charging station types, charging stations, and connectors. Provides security through JWT user authentication and password hashing. It includes comprehensive tests and documentation via Swagger UI.

## Built With

* FastAPI,
* Pytest,
* alembic,
* passlib,
* python-jose,
* PostgreSQL,
* Docker.



<!-- GETTING STARTED -->
# Getting Started

## Prerequisites

To run the API you will need:
* Git,
* Docker.

## Installation

1. Clone the repo
   
   ```sh
   git clone https://github.com/jmroczkowski99/EVChargingStation.git
   ```
   
2. Create an .env file containing database and test database info, secret key and hashing algorithm. Make sure that your database info matches your database URLs.
   If you don't want to run the API using Docker, make sure to install the requirements using pip and change database urls to support localhost.
   
   ```
   DATABASE_URL=postgresql://postgres:postgres@evchargingstation_db:5432/EVChargingStation
   TEST_DATABASE_URL=postgresql://postgres:postgres@test_db:5432/testdb
   SECRET_KEY=08d23e024faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
   ALGORITHM=HS256
   PG_USER=postgres
   PG_PASSWORD=postgres
   PG_DB=EVChargingStation
   PG_TEST_USER=postgres
   PG_TEST_PASSWORD=postgres
   PG_TEST_DB=testdb
   ```
   
3. Run Docker Compose
   
   ```sh
   docker compose up
   ```
   
4. If you want to run tests on your device, run
   
   ```sh
   docker exec -it evchargingstation_container pytest
   ```



<!-- USAGE EXAMPLES -->
# Usage
## Authentication and authorization

To access the electrical vehicle charging station management system, you have to create a user and log in. To achieve that, simply POST your username and password at /users/ endpoint as shown below. After logging in, the JWT will be valid for 2 minutes. After that time you will need to log in again and get a new token to access the endpoints. Expired tokens are deleted from the cache automatically everytime the token is validated.
<br />
<div align="center">
  <img src="https://github.com/jmroczkowski99/EVChargingStation/assets/146372897/beebd588-75cb-419d-a02e-3755b946ad44" alt="Documentation">
</div>

## API documentation

You can access the Swagger UI based documentation and view all of the endpoints and possible query parameters at /docs/ url.
<br />
<div align="center">
  <img src="https://github.com/jmroczkowski99/EVChargingStation/assets/146372897/b9822418-eeec-41cb-b87b-db4ac26d78af" alt="Documentation">
</div>

## Users

You can create, update and delete users. Responses include only the username for safety. You can only update or delete your own account at /users/{yourusername} endpoint.

Example user .json response:
```json
{
  "username": "admin"
}
```

To create a new user to specify:
* Username - has to be unique,
* Password.

Example valid input:
```json
{
  "username": "admin",
  "password": "admin"
}
```

## Charging Station Types

On startup, the database is seeded with 5 charging station types. You can create, read, update and delete them if authorized.

### Create, Update

To create or update a charging station type you have to specify:
* Name - has to be unique,
* Plug Count - has to be greater than 0,
* Efficiency - float value between 0 and 100,
* Current Type - AC or DC,
* Charging Station Type ID (query parameter) - UUID, only for updating.

Example valid input:
```json
{
  "name": "Example Type",
  "plug_count": 2,
  "efficiency": 85.2,
  "current_type": "AC"
}
```

### Read

You can either fetch a singular charging station type by providing its UUID as a query parameter or fetch a list of all charging station types. UUIDs of charging stations assigned to respective types are also listed in the response.
When fetching a list of charging station types, you can provide these query parameters for filtering and pagination:
* plug_count,
* min_efficiency,
* max_efficiency,
* current_type,
* skip,
* limit.

Example .json response:
```json
{
  "name": "Type A",
  "plug_count": 2,
  "efficiency": 88.53,
  "current_type": "AC",
  "id": "5dca2a03-ef4b-4d5d-963c-b729da403230",
  "charging_stations": [
    {
      "id": "ec796615-1a6f-4ee6-953a-d61db42d5f82"
    }
  ]
}
```

### Delete

To delete a charging station type you have to specify:
* Charging Station Type ID (query parameter) - UUID.

You cannot delete a charging station type if there are any charging stations assigned to it. You have to either delete these stations or change their types first.

## Charging Stations

You can create, read, update and delete charging stations if authorized.

### Create, Update

To create or update a new charging station you have to specify:
* Name - has to be unique,
* Device ID (optional) - UUID, generated automatically if not provided,
* IP Address - has to unique and a valid IPv4 or IPv6 address,
* Firmware Version,
* Type ID - UUID of existing charging station type,
* A list of connectors with their unique names and their priority (True/False) - number of connectors cannot exceed the plug_count value provided in assigned charging station type and only one connector can have priority.
* Charging Station ID (query parameter) - UUID, only for updating.

The creation or update of a charging station also creates/updates connectors assigned to it, but you can also create and assign connectors on their own. This option is described in the "Connectors" section.

Example valid input:
```json
{
  "name": "Station",
  "ip_address": "50.53.178.51",
  "firmware_version": "1.0.2",
  "type_id": "5dca2a03-ef4b-4d5d-963c-b729da403230",
  "connectors": [
    {
      "name": "First Connector",
      "priority": true
    },
    {
      "name": "Second Connector",
      "priority": false
    }
  ]
}
```

### Read

You can either fetch a singular charging station by providing its UUID as a query parameter or fetch a list of all charging stations. Charging station type and connectors info is also available in the response.
You can't fetch a charging station or charging station list when one of the stations doesn't have a proper connector count. Make sure every station has as many connectors as stated in its charging station type.
When fetching a list of charging stations, you can provide these query parameters for filtering and pagination:
* plug_count,
* min_efficiency,
* max_efficiency,
* current_type,
* firmware_version,
* skip,
* limit.

Example .json response:
```json
{
    "name": "Station",
    "device_id": "346af0fe-b960-40bb-9870-9a3167e114a2",
    "ip_address": "50.53.178.51",
    "firmware_version": "1.0.2",
    "id": "ec796615-1a6f-4ee6-953a-d61db42d5f82",
    "type": {
      "name": "Type A",
      "plug_count": 2,
      "efficiency": 88.53,
      "current_type": "AC",
      "id": "5dca2a03-ef4b-4d5d-963c-b729da403230"
    },
    "connectors": [
      {
        "name": "First Connector",
        "priority": true,
        "id": "5e6983ec-78e3-4ce5-8543-d4f352535527",
        "charging_station_id": "ec796615-1a6f-4ee6-953a-d61db42d5f82"
      },
      {
        "name": "Second Connector",
        "priority": false,
        "id": "9d0f0add-a2e7-4a26-a5be-310ebba21760",
        "charging_station_id": "ec796615-1a6f-4ee6-953a-d61db42d5f82"
      }
    ]
  }
```

### Delete

To delete a charging station you have to specify:
* Charging Station ID (query parameter) - UUID.

## Connectors

You can create, read, update and delete connectors if authorized.

### Create, Update

To create or update a connector you have to specify:
* Name - has to be unique,
* Priority - True/False, if you are assigning a connector to a charging station, make sure that there is only one connector with priority,
* Charging Station ID (optional) - UUID, make sure that the charging station doesn't violate the connector count or priority constrain,
* Connector ID (query parameter) - UUID, only for updating.

Example valid input:
```json
{
  "name": "Connector",
  "priority": true,
  "charging_station_id": "ec796615-1a6f-4ee6-953a-d61db42d5f82"
}
```

### Read

You can either fetch a singular connector by providing its UUID as a query parameter or fetch a list of all connectors.
When fetching a list of connectors, you can provide these query parameters for filtering and pagination:
* priority,
* charging_station_id,
* skip,
* limit.

Example .json response:
```json
{
    "name": "First Connector",
    "priority": true,
    "id": "5e6983ec-78e3-4ce5-8543-d4f352535527",
    "charging_station_id": "ec796615-1a6f-4ee6-953a-d61db42d5f82"
  }
```

### Delete

To delete a connector you have to specify:
* Connector ID (query parameter) - UUID.

## Logging

API logs information to the standard output so that it is clear what is happening. The logs have a structure: "[time [log_level] [context]]: msg"

Example:
```
  [2024-04-21 14:37:27 [INFO] [api.utils.auth]]: Token validated successfully for user 'admin'.
  [2024-04-21 14:37:27 [INFO] [api.utils.auth]]: Successfully retrieved user 'admin' from the token.
  [2024-04-21 14:37:27 [INFO] [api.routers.connector_router]]: Attempting to create a connector with data: name='Connector' priority=True charging_station_id=UUID('ec796615-1a6f-4ee6-953a-d61db42d5f82').
  [2024-04-21 14:37:27 [INFO] [api.crud.crud]]: Checking connector priority constraint...
  [2024-04-21 14:37:27 [INFO] [api.crud.crud]]: Connector priority constraint not violated.
  [2024-04-21 14:37:27 [INFO] [api.crud.crud]]: Checking connector count constraint...
  [2024-04-21 14:37:27 [INFO] [api.crud.crud]]: Connector count constraint not violated.
  [2024-04-21 14:37:27 [INFO] [api.routers.connector_router]]: Successfully created a connector with ID: 265e46c4-eb02-49c1-859d-7dfdf570eaa0.
```
