import pytest
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the base URL from environment variables
BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:5000')

@pytest.fixture
def sample_vehicle():
    """Sample vehicle data for tests."""
    return {
        "vin": "1HGCM82633A123456",
        "manufacturer_name": "Honda",
        "description": "A reliable sedan",
        "horse_power": 200,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.99,
        "fuel_type": "Gasoline"
    }

@pytest.fixture
def invalid_vehicle():
    """Invalid vehicle data missing required fields."""
    return {
        "manufacturer_name": "Honda",
        "model_name": "Accord",
        # Missing 'vin', 'model_year', 'fuel_type'
    }

def test_home_endpoint():
    """Test the home endpoint."""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Vehicles API"}

def test_create_vehicle(sample_vehicle):
    """Test creating a new vehicle."""
    # Clean up before test
    requests.delete(f"{BASE_URL}/vehicle/{sample_vehicle['vin']}")
    
    response = requests.post(f"{BASE_URL}/vehicle", json=sample_vehicle)
    assert response.status_code == 201
    assert response.json()["message"] == "Vehicle added successfully"

def test_create_vehicle_with_malformed_json():
    """Test creating a vehicle with malformed JSON."""
    headers = {'Content-Type': 'application/json'}
    malformed_json = '{"vin": "1234", "manufacturer_name": "Test" '  # Missing closing brace
    response = requests.post(f"{BASE_URL}/vehicle", data=malformed_json, headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Bad Request"
    assert response.json()["message"] == "Invalid JSON data"

def test_create_vehicle_with_missing_fields(invalid_vehicle):
    """Test creating a vehicle missing required fields."""
    response = requests.post(f"{BASE_URL}/vehicle", json=invalid_vehicle)
    assert response.status_code == 422
    assert response.json()["error"] == "Unprocessable Entity"
    assert "vin" in response.json()["details"]
    assert "model_year" in response.json()["details"]
    assert "fuel_type" in response.json()["details"]

def test_create_vehicle_with_invalid_data_types():
    """Test creating a vehicle with invalid data types."""
    invalid_data = {
        "vin": "1HGCM82633A123456",
        "manufacturer_name": "Honda",
        "model_name": "Accord",
        "model_year": "Twenty Twenty",  # Invalid data type
        "fuel_type": "Gasoline"
    }
    response = requests.post(f"{BASE_URL}/vehicle", json=invalid_data)
    assert response.status_code == 422
    assert response.json()["error"] == "Unprocessable Entity"
    assert "model_year" in response.json()["details"]
    assert response.json()["details"]["model_year"] == "'model_year' must be an integer."

def test_get_vehicle_by_vin(sample_vehicle):
    """Test retrieving a vehicle by VIN."""
    vin = sample_vehicle["vin"]
    response = requests.get(f"{BASE_URL}/vehicle/{vin}")
    assert response.status_code == 200
    assert response.json()["vin"] == vin

def test_get_vehicle_not_found():
    """Test retrieving a vehicle that does not exist."""
    non_existent_vin = "NONEXISTENTVIN12345"
    response = requests.get(f"{BASE_URL}/vehicle/{non_existent_vin}")
    assert response.status_code == 404
    assert response.json()["error"] == "Vehicle not found"

def test_update_vehicle(sample_vehicle):
    """Test updating a vehicle."""
    vin = sample_vehicle["vin"]
    updated_data = {
        "manufacturer_name": "Honda",
        "description": "Updated description",
        "horse_power": 210,
        "model_name": "Accord",
        "model_year": 2021,
        "purchase_price": 26000.99,
        "fuel_type": "Hybrid"
    }
    response = requests.put(f"{BASE_URL}/vehicle/{vin}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Vehicle updated successfully"

def test_update_vehicle_with_invalid_data(sample_vehicle):
    """Test updating a vehicle with invalid data types."""
    vin = sample_vehicle["vin"]
    invalid_data = {
        "model_year": "Two Thousand Twenty-One",  # Invalid data type
        "horse_power": "Two Hundred Ten"          # Invalid data type
    }
    response = requests.put(f"{BASE_URL}/vehicle/{vin}", json=invalid_data)
    assert response.status_code == 422
    assert response.json()["error"] == "Unprocessable Entity"
    assert "model_year" in response.json()["details"]
    assert "horse_power" in response.json()["details"]

def test_delete_vehicle(sample_vehicle):
    """Test deleting a vehicle."""
    vin = sample_vehicle["vin"]
    response = requests.delete(f"{BASE_URL}/vehicle/{vin}")
    assert response.status_code == 204

    # Verify deletion
    verify_response = requests.get(f"{BASE_URL}/vehicle/{vin}")
    assert verify_response.status_code == 404

def test_delete_vehicle_not_found():
    """Test deleting a vehicle that does not exist."""
    non_existent_vin = "NONEXISTENTVIN12345"
    response = requests.delete(f"{BASE_URL}/vehicle/{non_existent_vin}")
    assert response.status_code == 404
    assert response.json()["error"] == "Vehicle not found"
