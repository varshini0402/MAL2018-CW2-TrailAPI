# app.py
# Main application entry point for TrailService API
# Initializes Flask server with Connexion and Swagger UI

from database import connex_app

# Add API endpoints from swagger.yml specification
connex_app.add_api("swagger.yml")

if __name__ == "__main__":
    # Run development server with debug mode enabled
    # Debug mode provides detailed error messages and auto-reload on code changes
   connex_app.run(host="0.0.0.0", port=5000)