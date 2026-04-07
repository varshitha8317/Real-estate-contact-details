"""
Real Estate Property Management API

This module provides a FastAPI backend for managing real estate properties.
It includes CRUD operations for properties stored in a MySQL database.

Features:
- Add new properties
- Retrieve all properties or filter by city/area
- Update existing properties
- Delete properties
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Database connection setup using environment variables
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Pydantic model for property data validation
class Property(BaseModel):
    name: str
    city: str
    area: str
    property_type: str   # plot / house
    price: int
    bedrooms: Optional[int] = None
    area_sqft: int
    status: str = "available"



@app.post("/properties")
def add_property(property: Property):
    """
    Add a new property to the database.

    Args:
        property (Property): Property data to be added

    Returns:
        dict: Success message
    """
    cursor = db.cursor()

    query = """
        INSERT INTO properties
        (name, city, area, property_type, price, bedrooms, area_sqft, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        property.name,
        property.city,
        property.area,
        property.property_type,
        property.price,
        property.bedrooms,
        property.area_sqft,
        property.status
    )

    cursor.execute(query, values)
    db.commit()

    return {"message": "Property added successfully"}



@app.get("/properties")
def get_all_properties():
    """
    Retrieve all properties from the database.

    Returns:
        list: List of all properties as dictionaries
    """
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM properties")
    return cursor.fetchall()



@app.get("/properties/city/{city}")
def get_by_city(city: str):
    """
    Retrieve all properties in a specific city.

    Args:
        city (str): Name of the city to filter by

    Returns:
        list: List of properties in the specified city

    Raises:
        HTTPException: If no properties are found in the city
    """
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM properties WHERE city=%s", (city,))
    result = cursor.fetchall()

    if not result:
        raise HTTPException(status_code=404, detail="No properties in this city")

    return result



@app.get("/properties/{city}/{area}")
def get_by_city_area(city: str, area: str):
    """
    Retrieve all properties in a specific city and area.

    Args:
        city (str): Name of the city
        area (str): Name of the area within the city

    Returns:
        list: List of properties in the specified city and area

    Raises:
        HTTPException: If no properties are found
    """
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM properties WHERE city=%s AND area=%s",
        (city, area)
    )

    result = cursor.fetchall()

    if not result:
        raise HTTPException(status_code=404, detail="No properties found")

    return result



@app.put("/properties/{id}")
def update_property(id: int, property: Property):
    """
    Update an existing property by ID.

    Args:
        id (int): Property ID to update
        property (Property): Updated property data

    Returns:
        dict: Success message

    Raises:
        HTTPException: If property with given ID is not found
    """
    cursor = db.cursor()

    query = """
        UPDATE properties
        SET name=%s,
            city=%s,
            area=%s,
            property_type=%s,
            price=%s,
            bedrooms=%s,
            area_sqft=%s,
            status=%s
        WHERE id=%s
    """

    values = (
        property.name,
        property.city,
        property.area,
        property.property_type,
        property.price,
        property.bedrooms,
        property.area_sqft,
        property.status,
        id
    )

    cursor.execute(query, values)
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Property not found")

    return {"message": "Property updated successfully"}


@app.delete("/properties/{id}")
def delete_property(id: int):
    """
    Delete a property by ID.

    Args:
        id (int): Property ID to delete

    Returns:
        dict: Success message

    Raises:
        HTTPException: If property with given ID is not found
    """
    cursor = db.cursor()

    cursor.execute("DELETE FROM properties WHERE id=%s", (id,))
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Property not found")

    return {"message": "Property deleted successfully"}