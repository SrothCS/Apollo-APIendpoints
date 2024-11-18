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
            # You may log the error or exit the application gracefully if necessary
            return  # Exit the application if the database initialization fails
    else:
        print("Skipping database initialization in production.")

    print("Starting the Flask application...")
    # Bind to the host and port required by Heroku
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    main()
