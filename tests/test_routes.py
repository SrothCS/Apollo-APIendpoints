import pytest
from api.routes import app, initialize_database, get_db_connection

@pytest.fixture
def client():
    """Set up a Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            initialize_database()  # Reinitialize the database schema
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE vehicles_schema.vehicles RESTART IDENTITY CASCADE;")
            conn.commit()
            cursor.close()
            conn.close()
        yield client

@pytest.fixture
def add_test_vehicle():
    """Add a test vehicle to the database."""
    test_vehicle = {
        "vin": "1HGCM82633A123456",
        "manufacturer_name": "Honda",
        "description": "A reliable sedan",
        "horse_power": 200,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.99,
        "fuel_type": "Gasoline"
    }
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO vehicles_schema.vehicles (vin, manufacturer_name, description, horse_power, model_name, model_year, purchase_price, fuel_type)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_query, tuple(test_vehicle.values()))
    conn.commit()
    cursor.close()
    conn.close()
    return test_vehicle

def test_home(client):
    """Test the home endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Vehicles API"}

def test_create_vehicle(client):
    """Test creating a new vehicle."""
    vehicle_data = {
        "vin": "1HGCM82633A654321",
        "manufacturer_name": "Toyota",
        "description": "A compact car",
        "horse_power": 150,
        "model_name": "Corolla",
        "model_year": 2021,
        "purchase_price": 20000.00,
        "fuel_type": "Gasoline"
    }
    response = client.post('/vehicle', json=vehicle_data)
    assert response.status_code == 201
    assert response.json["message"] == "Vehicle added successfully"

    # Verify the vehicle was added
    get_response = client.get(f'/vehicle/{vehicle_data["vin"]}')
    assert get_response.status_code == 200
    assert get_response.json["vin"] == vehicle_data["vin"]

def test_get_vehicles(client, add_test_vehicle):
    """Test fetching all vehicles."""
    response = client.get('/vehicle')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert any(vehicle["vin"] == add_test_vehicle["vin"] for vehicle in response.json)

def test_get_vehicle_by_vin(client, add_test_vehicle):
    """Test fetching a vehicle by VIN."""
    response = client.get(f'/vehicle/{add_test_vehicle["vin"]}')
    assert response.status_code == 200
    assert response.json["vin"] == add_test_vehicle["vin"]

def test_update_vehicle(client, add_test_vehicle):
    """Test updating a vehicle."""
    updated_data = {
        "manufacturer_name": "Honda",
        "description": "Updated description",
        "horse_power": 210,
        "model_name": "Accord",
        "model_year": 2021,
        "purchase_price": 26000.99,
        "fuel_type": "Hybrid"
    }
    response = client.put(f'/vehicle/{add_test_vehicle["vin"]}', json=updated_data)
    assert response.status_code == 200
    assert response.json["message"] == "Vehicle updated successfully"

    # Verify the updates were applied
    get_response = client.get(f'/vehicle/{add_test_vehicle["vin"]}')
    assert get_response.status_code == 200
    for key, value in updated_data.items():
        assert get_response.json[key] == value

def test_delete_vehicle(client, add_test_vehicle):
    """Test deleting a vehicle by VIN."""
    response = client.delete(f'/vehicle/{add_test_vehicle["vin"]}')
    assert response.status_code == 204

    # Verify the vehicle was deleted
    get_response = client.get(f'/vehicle/{add_test_vehicle["vin"]}')
    assert get_response.status_code == 404

def test_create_vehicle_invalid_data(client):
    """Test creating a vehicle with invalid data."""
    invalid_vehicle_data = {
        "manufacturer_name": "Ford",  # Missing required fields
        "model_year": 2020,
        "fuel_type": "Gasoline"
    }
    response = client.post('/vehicle', json=invalid_vehicle_data)
    assert response.status_code == 422
    assert "message" in response.json
    assert "is required" in response.json["message"]

def test_get_vehicle_not_found(client):
    """Test fetching a non-existent vehicle by VIN."""
    response = client.get('/vehicle/INVALID_VIN')
    assert response.status_code == 404
    assert response.json["error"] == "Vehicle not found"

