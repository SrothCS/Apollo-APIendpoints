from flask import Flask, request, jsonify
from psycopg2 import connect, sql, Error
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env (for local development)
load_dotenv()

app = Flask(__name__)

# Database connection configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # Parse DATABASE_URL
    parsed_url = urlparse(DATABASE_URL)
    DB_CONFIG = {
        "dbname": parsed_url.path[1:],  # Remove leading '/'
        "user": parsed_url.username,
        "password": parsed_url.password,
        "host": parsed_url.hostname,
        "port": parsed_url.port,
    }
else:
    # Handle case when DATABASE_URL is not set
    raise Exception("DATABASE_URL environment variable not set")

def get_db_connection():
    """Establish a database connection."""
    try:
        # Determine SSL mode based on the environment
        sslmode = "require" if os.getenv("ENV") == "production" else "disable"
        return connect(sslmode=sslmode, **DB_CONFIG)
    except Error as e:
        print(f"Error connecting to the database: {e}")
        raise

def initialize_database():
    """Initialize the database schema."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create the schema without specifying AUTHORIZATION
        cursor.execute("CREATE SCHEMA IF NOT EXISTS vehicles_schema;")

        # Create the vehicles table within the schema
        create_table_query = """
        CREATE TABLE IF NOT EXISTS vehicles_schema.vehicles (
            vin VARCHAR(17) PRIMARY KEY,
            manufacturer_name VARCHAR(255) NOT NULL,
            description TEXT,
            horse_power INT,
            model_name VARCHAR(255) NOT NULL,
            model_year INT NOT NULL,
            purchase_price DECIMAL(10, 2),
            fuel_type VARCHAR(50) NOT NULL
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
    except Error as e:
        print(f"Error initializing database: {e}")
        raise

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad Request", "message": "Invalid JSON data"}), 400

@app.errorhandler(422)
def unprocessable_entity(e):
    return jsonify({"error": "Unprocessable Entity", "message": "Validation failed", "details": str(e)}), 422

@app.route('/', methods=['GET'])
def home():
    """Home route to verify the API is running."""
    return jsonify({"message": "Welcome to the Vehicles API"}), 200

@app.route('/vehicle', methods=['GET'])
def get_vehicles():
    """Fetch all vehicle records."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles_schema.vehicles;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        vehicles = [
            {
                "vin": row[0],
                "manufacturer_name": row[1],
                "description": row[2],
                "horse_power": row[3],
                "model_name": row[4],
                "model_year": row[5],
                "purchase_price": float(row[6]) if row[6] else None,
                "fuel_type": row[7],
            }
            for row in rows
        ]
        return jsonify(vehicles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    """Add a new vehicle."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Bad Request", "message": "No JSON data provided"}), 400

        required_fields = ["vin", "manufacturer_name", "model_name", "model_year", "fuel_type"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": "Unprocessable Entity", "message": f"'{field}' is required"}), 422

        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO vehicles_schema.vehicles (vin, manufacturer_name, description, horse_power, model_name, model_year, purchase_price, fuel_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (
            data["vin"],
            data["manufacturer_name"],
            data.get("description"),
            data.get("horse_power"),
            data["model_name"],
            data["model_year"],
            data.get("purchase_price"),
            data["fuel_type"],
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Vehicle added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/vehicle/<string:vin>', methods=['GET'])
def get_vehicle_by_vin(vin):
    """Fetch a vehicle by VIN."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles_schema.vehicles WHERE vin = %s;", (vin,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return jsonify({"error": "Vehicle not found"}), 404

        vehicle = {
            "vin": row[0],
            "manufacturer_name": row[1],
            "description": row[2],
            "horse_power": row[3],
            "model_name": row[4],
            "model_year": row[5],
            "purchase_price": float(row[6]) if row[6] else None,
            "fuel_type": row[7],
        }
        return jsonify(vehicle), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/vehicle/<string:vin>', methods=['PUT'])
def update_vehicle(vin):
    """Update a vehicle record."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Bad Request", "message": "No JSON data provided"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        update_query = """
        UPDATE vehicles_schema.vehicles
        SET manufacturer_name = %s, description = %s, horse_power = %s,
            model_name = %s, model_year = %s, purchase_price = %s, fuel_type = %s
        WHERE vin = %s;
        """
        cursor.execute(update_query, (
            data.get("manufacturer_name"),
            data.get("description"),
            data.get("horse_power"),
            data.get("model_name"),
            data.get("model_year"),
            data.get("purchase_price"),
            data.get("fuel_type"),
            vin
        ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Vehicle updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/vehicle/<string:vin>', methods=['DELETE'])
def delete_vehicle(vin):
    """Delete a vehicle record."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vehicles_schema.vehicles WHERE vin = %s;", (vin,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Vehicle deleted successfully"}), 204
    except Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Only initialize the database in development
    if os.getenv("ENV") != "production":
        initialize_database()
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
