# Vehicle Management API
This project is a Vehicle Management API that allows users to perform CRUD (Create, Read, Update, Delete) operations on a PostgreSQL database of vehicle records. It provides RESTful endpoints to manage vehicle data such as adding, deleting, updating, and retrieving vehicle information.


## Features

- Retrieve All Vehicles: Fetch all vehicle records stored in the database.
- Retrieve a Vehicle by VIN: Fetch details of a specific vehicle using its unique VIN.
- Add a New Vehicle: Add a new vehicle record to the database.
- Update Vehicle Information: Modify details of an existing vehicle.
- Delete a Vehicle: Remove a vehicle record from the database.

---

## Endpoints

| HTTP Method | Endpoint           | Description                  |
|-------------|--------------------|------------------------------|
| `GET`       | `/vehicle`         | Fetch all vehicle records    |
| `POST`      | `/vehicle`         | Add a new vehicle record     |
| `GET`       | `/vehicle/{vin}`   | Fetch a vehicle by its VIN   |
| `PUT`       | `/vehicle/{vin}`   | Update an existing vehicle   |
| `DELETE`    | `/vehicle/{vin}`   | Delete a vehicle by its VIN  |

---

## Setup Instructions

### 1. Prerequisites
- Python 3.x installed
- PostgreSQL installed
- `curl` (optional, for testing the API)


### 2. Setting Up PostgreSQL
1. Log in as the `postgres` user:
   ```bash
   sudo -u postgres psql
   ```

2. Create the database and user:
   ```bash
   CREATE DATABASE vehicles_db;
   CREATE USER vehicles_user WITH PASSWORD 'vehicles_password';
   GRANT ALL PRIVILEGES ON DATABASE vehicles_db TO vehicles_user;
   ```

   than exit using:
   ```
   \q
   ```

3. Log into the database with created user:
   ```bash
   psql -h localhost -U vehicles_user -d vehicles_db
   ```

4. Create the schema:
   ```bash
   CREATE SCHEMA vehicles_schema AUTHORIZATION vehicles_user;
   ```

5. Grant privileges:
   ```bash
   GRANT USAGE, CREATE ON SCHEMA vehicles_schema TO vehicles_user;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA vehicles_schema TO vehicles_user;
   ```

### 3. Clone and Set Up the Project

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CommandLineAPI
   ```

2. Install dependencies and initialize the database:
   ```bash
   make
   ```

## Running the API

1. Start the Flask application:
   ```bash
   make run
   ```

<img src="https://github.com/user-attachments/assets/28cec15f-e479-49c9-b6ea-57f8f178ea1a" alt="image" width="300"/> 

   
2. Open a new terminal tab to run queries against the API.

### Example Queries Using `curl`

Fetch All Vehicles:

```bash
curl -X GET http://127.0.0.1:5000/vehicle
```

<img src="https://github.com/user-attachments/assets/da3dde9e-a84e-4f9e-8821-f84ad3cce82a" alt="image" width="600"/> 

Add a New Vehicle:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "vin": "1HGCM82633A123459",
    "manufacturer_name": "Lamborguini",
    "description": "A expensive cool car",
    "horse_power": 20000,
    "model_name": "huracan",
    "model_year": 2020,
    "purchase_price": 25000.99,
    "fuel_type": "Petrol"
}' http://127.0.0.1:5000/vehicle
```

<img src="https://github.com/user-attachments/assets/f09b0355-261d-47eb-b886-80d0fdae787e" alt="image" width="600"/> 

Fetch a Vehicle by VIN:

```bash
curl -X GET http://127.0.0.1:5000/vehicle/1HGCM82633A123459
```

<img src="https://github.com/user-attachments/assets/cf30fe63-b949-4e94-8653-4760ccb0e155" alt="image" width="600"/> 

Update Vehicle Information:

```bash
curl -X PUT -H "Content-Type: application/json" -d '{
    "vin": "1HGCM82633A123459",
    "manufacturer_name": "Lamborguini",
    "description": "A expensive cool car",
    "horse_power": 20000,
    "model_name": "aventador",
    "model_year": 2020,
    "purchase_price": 25000.99,
    "fuel_type": "Petrol"
}' http://127.0.0.1:5000/vehicle/1HGCM82633A123456

```

<img src="https://github.com/user-attachments/assets/26007b5e-6024-4150-8b98-966542175d07" alt="image" width="600"/> 

Delete a Vehicle:

```bash
curl -X DELETE http://127.0.0.1:5000/vehicle/1HGCM82633A123459
```

<img src="https://github.com/user-attachments/assets/bf3bbf2d-d392-411b-a809-f521afd5a70f" alt="image" width="600"/> 

---

## Available Makefile Commands

| Command       | Description                                    |
|---------------|------------------------------------------------|
| `make`        | Installs dependencies and initializes the database |
| `make run`    | Runs the Flask application                    |
| `make test`   | Runs example `curl` commands to test the API  |
| `make clean`  | Cleans the virtual environment and dependencies |

---

## Project Flow

1. **Set up PostgreSQL:** Follow the PostgreSQL setup instructions below to prepare the database.
2. **Run the Flask server:** Start the application using `make run`.
3. **Test API Endpoints:** Use the provided `curl` commands to add, fetch, update, or delete vehicle records.
4. **View Results:** Query the database to verify changes made by the API.

---

## Notes

- The VIN (Vehicle Identification Number) is a unique key for each vehicle.
- Ensure the Flask server is running in one terminal tab while using another terminal for curl queries.
- Errors will return JSON responses with detailed error messages.

- ## Testing Commands

Below are detailed `curl` commands to test each endpoint with both **valid (good)** and **invalid (bad)** scenarios.

### 1. Home Endpoint (`GET /`)

#### a. **Good Request**

**Description:** Verify that the API is running and responds with a welcome message.


curl -X GET http://vehicles-management-1235f3bf9a83.herokuapp.com/
Expected Response:
	•	Status Code: 200 OK
	•	Body: {
  "message": "Welcome to the Vehicles API"
}
b. Bad Request

Attempting to send a method not allowed on this endpoint.

Command: curl -X POST http://vehicles-management-1235f3bf9a83.herokuapp.com/

Expected Response:
	•	Status Code: 405 Method Not Allowed
	•	Body: {
  "error": "Method Not Allowed",
  "message": "The method is not allowed for the requested URL."
}
2. Fetch All Vehicles (GET /vehicle)

a. Good Request

Description: Retrieve all vehicle records from the database.

Command: curl -X GET http://vehicles-management-1235f3bf9a83.herokuapp.com/vehicle

Expected Response:
	•	Status Code: 200 OK
	•	Body: JSON array of vehicle objects.
[
  {
    "vin": "1HGCM82633A123456",
    "manufacturer_name": "Honda",
    "model_name": "Accord",
    "model_year": 2020,
    "fuel_type": "Gasoline",
    "description": "A reliable sedan",
    "horse_power": 200,
    "purchase_price": 25000.99
  },
  ...
  ]
  b. Bad Request

Fetching all vehicles typically doesn’t have a bad request scenario unless additional parameters are expected.

3. Add a New Vehicle (POST /vehicle)

a. Good Request

Description: Add a new vehicle record with all required fields.

Command: curl -X POST http://vehicles-management-1235f3bf9a83.herokuapp.com/vehicle \
     -H "Content-Type: application/json" \
     -d '{
           "vin": "1HGCM82633A123459",
           "manufacturer_name": "Lamborghini",
           "model_name": "Huracan",
           "model_year": 2020,
           "fuel_type": "Petrol",
           "description": "A fast cool car",
           "horse_power": 500,
           "purchase_price": 25000.99
         }'
Expected Response:
	•	Status Code: 201 Created
	•	Body: {
  "message": "Vehicle added successfully",
  "vehicle": {
    "vin": "1HGCM82633A123459",
    "manufacturer_name": "Lamborghini",
    "model_name": "Huracan",
    "model_year": 2020,
    "fuel_type": "Petrol",
    "description": "A fast cool car",
    "horse_power": 500,
    "purchase_price": 25000.99
  }
}
b. Bad Requests

i. Missing Required Fields

Description: Attempt to add a vehicle without providing all required fields (e.g., missing vin).

Command: curl -X POST http://vehicles-management-1235f3bf9a83.herokuapp.com/vehicle \
     -H "Content-Type: application/json" \
     -d '{
           "manufacturer_name": "Toyota",
           "model_name": "Camry",
           "model_year": 2010,
           "fuel_type": "Gasoline"
         }'
Expected Response:
	•	Status Code: 422 Unprocessable Entity
	•	Body: {
  "error": "Unprocessable Entity",
  "message": "Validation failed",
  "details": {
    "vin": "'vin' is required."
  }
}
ii. Invalid Data Types

Description: Attempt to add a vehicle with incorrect data types (e.g., model_year as a string).

Command: curl -X POST http://vehicles-management-1235f3bf9a83.herokuapp.com/vehicle \
     -H "Content-Type: application/json" \
     -d '{
           "vin": "1HGCM82633A123460",
           "manufacturer_name": "Ford",
           "model_name": "Mustang",
           "model_year": "Two Thousand Ten",
           "fuel_type": "Gasoline"
         }'
     Expected Response:
	•	Status Code: 422 Unprocessable Entity
	•	Body: {
  "error": "Unprocessable Entity",
  "message": "Validation failed",
  "details": {
    "model_year": "'model_year' must be an integer."
  }
}
iii. Duplicate VIN

Description: Attempt to add a vehicle with a VIN that already exists in the database.

Command: curl -X POST http://vehicles-management-1235f3bf9a83.herokuapp.com/vehicle \
     -H "Content-Type: application/json" \
     -d '{
           "vin": "1HGCM82633A123459",
           "manufacturer_name": "Ferrari",
           "model_name": "F8",
           "model_year": 2021,
           "fuel_type": "Petrol",
           "description": "A luxury sports car",
           "horse_power": 710,
           "purchase_price": 28000.99
         }'
Expected Response:
	•	Status Code: 409 Conflict
	•	Body: {
  "error": "Conflict",
  "message": "A vehicle with this VIN already exists."
}

4. Fetch a Vehicle by VIN (GET /vehicle/{vin})

a. Good Request

Description: Retrieve details of an existing vehicle using its VIN.

Command: curl -X GET http://vehicles-management-1235f3bf9a83.herokuapp.com/vehicle/1HGCM82633A123459
Expected Response:
	•	Status Code: 200 OK
b. Bad Requests

i. Non-Existent VIN

Description: Attempt to retrieve a vehicle that does not exist in the database.

Command: curl -X GET http://vehicles-management-1235f3bf9a83.herokuapp.com/vehicle/NONEXISTENTVIN123

5. Update a Vehicle (PUT /vehicle/{vin})

a. Good Request

Description: Update specific details of an existing vehicle.

Command: curl -X PUT http://vehicles-management-1235f3bf9a83.herokuapp.com/vehicle/1HGCM82633A123459 \
     -H "Content-Type: application/json" \
     -d '{
           "description": "An updated description for the Huracan",
           "model_year": 2021,
           "horse_power": 550
         }'




