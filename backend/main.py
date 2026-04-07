from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import mysql.connector

app = FastAPI()

# MySQL connection
db = mysql.connector.connect(
    host="172.25.84.112",
    user="teamuser",
    password="team123",
    database="realestate_db"
)

class Property(BaseModel):
    name: str
    city: str
    area: str
    property_type: str
    price: int
    bedrooms: Optional[int] = None
    area_sqft: int
    status: str = "available"


# POST endpoint → Add property
@app.post("/properties")
def add_property(property: Property):
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

    return {
        "message": "Property added successfully",
        "property_id": cursor.lastrowid
    }


# PUT endpoint → Update property by name
@app.put("/properties/{name}")
def update_property(name: str, property: Property):
    cursor = db.cursor()

    query = """
        UPDATE properties
        SET city=%s,
            area=%s,
            property_type=%s,
            price=%s,
            bedrooms=%s,
            area_sqft=%s,
            status=%s
        WHERE name=%s
    """

    values = (
        property.city,
        property.area,
        property.property_type,
        property.price,
        property.bedrooms,
        property.area_sqft,
        property.status,
        name
    )

    cursor.execute(query, values)
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    return {"message": "Property updated successfully"}