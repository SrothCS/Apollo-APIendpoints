from api.routes import app, initialize_database
import os

def main():
    """Main entry point for the application."""
    try:
        print("Initializing the database...")
        initialize_database()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        # You may log the error or exit the application gracefully if necessary
        return  # Exit the application if the database initialization fails

    print("Starting the Flask application...")
    # Bind to the host and port required by Heroku
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    main()

