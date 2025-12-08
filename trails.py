# trails.py
# API endpoint handlers for Trail CRUD operations
# Implements business logic with authentication integration

from flask import abort, make_response
import requests
from database import db
from models import Trail, trails_schema, trail_schema


def read_all():
    """Retrieve all trails from database"""
    trails = Trail.query.all()
    return trails_schema.dump(trails)


def read_one(trail_id):
    """Retrieve single trail by ID"""
    trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()
    
    if trail is not None:
        return trail_schema.dump(trail)
    else:
        abort(404, f"Trail with ID {trail_id} not found")


def create(body):
    """Create new trail after authentication verification"""
    email = body.get("email")
    password = body.get("password")
    
    if not email or not password:
        abort(401, "Authentication credentials required")
    
    # Verify credentials with authentication service
    auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
    auth_response = requests.post(auth_url, json={"email": email, "password": password})
    
    if auth_response.status_code != 200:
        abort(401, "Authentication failed")
    
    # Remove authentication fields before creating trail
    trail_data = {k: v for k, v in body.items() if k not in ['email', 'password']}
    
    # Check for duplicate trail names
    trail_name = trail_data.get("Trail_Name")
    existing_trail = Trail.query.filter(Trail.Trail_Name == trail_name).one_or_none()
    
    if existing_trail is None:
        new_trail = trail_schema.load(trail_data, session=db.session)
        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.dump(new_trail), 201
    else:
        abort(406, f"Trail with name {trail_name} already exists")


def update(trail_id, body):
    """Update existing trail after authentication"""
    email = body.get("email")
    password = body.get("password")
    
    if not email or not password:
        abort(401, "Authentication credentials required")
    
    auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
    auth_response = requests.post(auth_url, json={"email": email, "password": password})
    
    if auth_response.status_code != 200:
        abort(401, "Authentication failed")
    
    existing_trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()
    
    if existing_trail:
        # Remove authentication fields before updating
        trail_data = {k: v for k, v in body.items() if k not in ['email', 'password']}
        
        # Update trail attributes
        update_trail = trail_schema.load(trail_data, session=db.session)
        existing_trail.Trail_Name = update_trail.Trail_Name
        existing_trail.Trail_Summary = update_trail.Trail_Summary
        existing_trail.Difficulty = update_trail.Difficulty
        existing_trail.Location = update_trail.Location
        existing_trail.Length = update_trail.Length
        existing_trail.Elevation_Gain = update_trail.Elevation_Gain
        existing_trail.Start_Point = update_trail.Start_Point
        existing_trail.End_Point = update_trail.End_Point
        existing_trail.Estimated_Time = update_trail.Estimated_Time
        existing_trail.Accessibility = update_trail.Accessibility
        existing_trail.Surface_Type = update_trail.Surface_Type
        
        db.session.merge(existing_trail)
        db.session.commit()
        return trail_schema.dump(existing_trail), 200
    else:
        abort(404, f"Trail with ID {trail_id} not found")


def delete(trail_id):
    """Remove trail from database after authentication"""
    existing_trail = Trail.query.filter(Trail.Trail_ID == trail_id).one_or_none()
    
    if existing_trail:
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(f"Trail {trail_id} successfully deleted", 200)
    else:
        abort(404, f"Trail with ID {trail_id} not found")