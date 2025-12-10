# TrailService REST API

Trail Management RESTful API - MAL2018 Assessment 2

## Project Overview

TrailService is a Python-based REST API microservice that provides programmatic access to trail information stored in a SQL Server database. The API supports CRUD operations for trail management with authentication integration through the university's central authentication service.

## Technologies Used

- **Python 3.14**
- **Flask** - Web framework
- **Connexion** - API framework with OpenAPI/Swagger support
- **SQLAlchemy** - Object-Relational Mapping
- **Marshmallow** - Data serialization and validation
- **pyodbc** - SQL Server database connectivity

## Database Schema

The API uses the CW2 schema on dist-6-505.uopnet.plymouth.ac.uk with the following tables:
- Trail (main entity)
- RouteType (trail categories)
- Location (geographical data)
- TrailRoute (junction table)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/varshini0402/MAL2017-CW2-TrailAPI.git
cd MAL2017-CW2-TrailAPI
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure database credentials in `config.py`:
   - Update DATABASE name
   - Update UID (username)
   - Update PWD (password)

## Running the API

Start the development server:
```bash
python app.py
```

The API will be available at: `http://localhost:5000/api`

Swagger documentation: `http://localhost:5000/api/ui`

## API Endpoints

### Public Endpoints (No Authentication)
- `GET /api/trails` - Retrieve all trails
- `GET /api/trails/{trail_id}` - Retrieve single trail

### Protected Endpoints (Authentication Required)
- `POST /api/trails` - Create new trail
- `PUT /api/trails/{trail_id}` - Update trail
- `DELETE /api/trails/{trail_id}` - Delete trail

Authentication is performed through the university service at:
`https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users`

## Project Structure
```
MAL2017_TrailService/
├── app.py                 # Main application entry point
├── config.py              # Database configuration
├── models.py              # SQLAlchemy models and schemas
├── trails.py              # API endpoint handlers
├── swagger.yml            # OpenAPI specification
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Authentication

Protected endpoints require email and password in the request body:
```json
{
  "TrailName": "Example Trail",
  "LocationID": 1,
  "OwnerID": 1,
  "email": "user@plymouth.ac.uk",
  "password": "password123"
}
```

## Deployment

The API is deployed on the university server at:
`https://web.socem.plymouth.ac.uk/[your-path]/api`

## Author

**Student Name:** Varshini
**Student ID:** BSSE2506011
**Module:** MAL2018 Information Management & Retrieval
**Assessment:** CW2 - REST API Development

## GitHub Repository

Repository shared with:
- mjread
- haoyiwang25
