# Define variables
PYTHON = python3
PIP = pip3
APP = main.py
VENV_DIR = venv
REQUIREMENTS = requirements.txt

# Default target: Install and run the app
all: install run

# Create a virtual environment and install dependencies
install:
	@echo "Creating virtual environment..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		$(PYTHON) -m venv $(VENV_DIR); \
		echo "Virtual environment created."; \
	else \
		echo "Virtual environment already exists. Skipping creation."; \
	fi
	@echo "Activating virtual environment and installing dependencies..."
	. $(VENV_DIR)/bin/activate && $(PIP) install --upgrade pip && $(PIP) install -r $(REQUIREMENTS)

# Run the Flask application
run:
	@echo "Initializing the database..."
	. $(VENV_DIR)/bin/activate && $(PYTHON) -c "from api.routes import initialize_database; initialize_database()"
	@echo "Running the Flask application..."
	. $(VENV_DIR)/bin/activate && $(PYTHON) $(APP)

# Test the Flask application using pytest
pytest:
	@echo "Running pytest..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Virtual environment not found. Run 'make install' first."; \
		exit 1; \
	fi
	. $(VENV_DIR)/bin/activate && PYTHONPATH=$(PWD) pytest --cov=api tests/

# Test the Flask application using curl commands
test:
	@echo "Testing the application..."
	curl -X GET http://127.0.0.1:5000/vehicle || echo "GET request failed."
	curl -X POST -H "Content-Type: application/json" -d '{"vin":"1HGCM82633A123456","manufacturer_name":"Honda","description":"A reliable sedan","horse_power":200,"model_name":"Accord","model_year":2020,"purchase_price":25000.99,"fuel_type":"Gasoline"}' http://127.0.0.1:5000/vehicle || echo "POST request failed."
	curl -X GET http://127.0.0.1:5000/vehicle/1HGCM82633A123456 || echo "GET by VIN request failed."
	curl -X PUT -H "Content-Type: application/json" -d '{"manufacturer_name":"Honda","description":"Updated description","horse_power":210,"model_name":"Accord","model_year":2021,"purchase_price":26000.99,"fuel_type":"Hybrid"}' http://127.0.0.1:5000/vehicle/1HGCM82633A123456 || echo "PUT request failed."
	curl -X DELETE http://127.0.0.1:5000/vehicle/1HGCM82633A123456 || echo "DELETE request failed."

# Clean up the environment
clean:
	@echo "Cleaning up virtual environment..."
	rm -rf $(VENV_DIR)
	@echo "Virtual environment removed."
