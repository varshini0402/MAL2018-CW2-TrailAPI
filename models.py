# models.py
# Database models matching CW1 table structure adapted for CW2 schema
# Defines Trail, RouteType, and TrailRoute entities

import pytz
from datetime import datetime
from marshmallow_sqlalchemy import fields
from database import db, ma


class RouteType(db.Model):
    """Route type categories for trails"""
    __tablename__ = "ROUTE_TYPES"
    __table_args__ = {'schema': 'CW2'}
    
    Route_Type_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Route_Type = db.Column(db.String(50), nullable=False, unique=True)
    
    trail_routes = db.relationship('TrailRoute', backref='route_type', cascade='all, delete-orphan')


class Trail(db.Model):
    """Main trail entity containing all trail information"""
    __tablename__ = "TRAILS"
    __table_args__ = {'schema': 'CW2'}
    
    Trail_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Trail_Name = db.Column(db.String(100), nullable=False)
    Trail_Summary = db.Column(db.String(255))
    Difficulty = db.Column(db.String(20))
    Location = db.Column(db.String(100))
    Length = db.Column(db.Numeric(5, 2))
    Elevation_Gain = db.Column(db.Integer)
    Start_Point = db.Column(db.String(150))
    End_Point = db.Column(db.String(150))
    Estimated_Time = db.Column(db.Numeric(4, 1))
    Accessibility = db.Column(db.String(255))
    Surface_Type = db.Column(db.String(50))
    Owner_ID = db.Column(db.Integer, nullable=False, default=1)
    Created_At = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kuala_Lumpur')))
    Updated_At = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kuala_Lumpur')),
                          onupdate=lambda: datetime.now(pytz.timezone('Asia/Kuala_Lumpur')))
    
    trail_routes = db.relationship('TrailRoute', backref='trail', cascade='all, delete-orphan')


class TrailRoute(db.Model):
    """Links trails with their route types"""
    __tablename__ = "TRAIL_ROUTES"
    __table_args__ = {'schema': 'CW2'}
    
    Route_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Trail_ID = db.Column(db.Integer, db.ForeignKey('CW2.TRAILS.Trail_ID'), nullable=False)
    Route_Type_ID = db.Column(db.Integer, db.ForeignKey('CW2.ROUTE_TYPES.Route_Type_ID'), nullable=False)
    Route_Notes = db.Column(db.String(255))


class RouteTypeSchema(ma.SQLAlchemyAutoSchema):
    """Serialization schema for RouteType"""
    class Meta:
        model = RouteType
        load_instance = True
        sqla_session = db.session


class TrailSchema(ma.SQLAlchemyAutoSchema):
    """Serialization schema for Trail"""
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
        include_fk = True


class TrailRouteSchema(ma.SQLAlchemyAutoSchema):
    """Serialization schema for TrailRoute"""
    class Meta:
        model = TrailRoute
        load_instance = True
        sqla_session = db.session


# Schema instances for API endpoints
route_type_schema = RouteTypeSchema()
route_types_schema = RouteTypeSchema(many=True)

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)

trail_route_schema = TrailRouteSchema()
trail_routes_schema = TrailRouteSchema(many=True)