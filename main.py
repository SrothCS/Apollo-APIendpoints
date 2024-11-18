from api.routes import app
import os

def main():
    """Main entry point for the application."""
    env = os.getenv("ENV", "").strip()
    print(f"ENV variable is: '{env}'")  # For debugging purposes

    if env != "production":
        try:
            print("Initializing the database...")
            from api.routes import initialize_database
            initialize_database()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize database: {e}")
            return  # Exit if database initialization fails

        print("Starting the Flask application...")
        app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        print("Skipping database initialization in production.")
        # Do not call app.run() here

if __name__ == "__main__":
    main()
