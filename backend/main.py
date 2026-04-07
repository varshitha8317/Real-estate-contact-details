from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Model
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
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM properties")
    return cursor.fetchall()



@app.get("/properties/city/{city}")
def get_by_city(city: str):
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM properties WHERE city=%s", (city,))
    result = cursor.fetchall()

    if not result:
        raise HTTPException(status_code=404, detail="No properties in this city")

    return result



@app.get("/properties/{city}/{area}")
def get_by_city_area(city: str, area: str):
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
    cursor = db.cursor()

    cursor.execute("DELETE FROM properties WHERE id=%s", (id,))
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Property not found")

    return {"message": "Property deleted successfully"}