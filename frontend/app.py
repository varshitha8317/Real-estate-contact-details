import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🏡 Real Estate App")

# =========================
# ➕ ADD PROPERTY
# =========================
st.header("Add Property")

name = st.text_input("Property Name")
city = st.text_input("City")
area = st.text_input("Area")

property_type = st.selectbox("Property Type", ["House", "Plot", "Apartment"])

price = st.number_input("Price", min_value=0)
bedrooms = st.number_input("Bedrooms", min_value=0, value=0)
area_sqft = st.number_input("Area (sqft)", min_value=0)

status = st.selectbox("Status", ["available", "sold"])

if st.button("Add Property"):
    data = {
        "name": name,
        "city": city,
        "area": area,
        "property_type": property_type,
        "price": int(price),
        "bedrooms": int(bedrooms) if bedrooms > 0 else None,
        "area_sqft": int(area_sqft),
        "status": status
    }

    response = requests.post(f"{API_URL}/properties", json=data)

    if response.status_code == 200:
        st.success("Property added successfully!")
    else:
        st.error("Error adding property")


# =========================
# 📋 VIEW ALL PROPERTIES
# =========================
st.header("All Properties")

if st.button("Show All"):
    response = requests.get(f"{API_URL}/properties")

    if response.status_code == 200:
        properties = response.json()
        st.write(properties)
    else:
        st.error("Error fetching data")


# =========================
# 🔍 FILTER BY CITY
# =========================
st.header("Search by City")

search_city = st.text_input("Enter City")

if st.button("Search City"):
    response = requests.get(f"{API_URL}/properties/city/{search_city}")

    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error("No properties found")


# =========================
# 🔍 FILTER BY CITY + AREA
# =========================
st.header("Search by City & Area")

search_city2 = st.text_input("City (filter)")
search_area = st.text_input("Area (filter)")

if st.button("Search Area"):
    response = requests.get(f"{API_URL}/properties/{search_city2}/{search_area}")

    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error("No properties found")


# =========================
# ❌ DELETE PROPERTY
# =========================
st.header("Delete Property")

delete_id = st.number_input("Enter Property ID", min_value=1)

if st.button("Delete"):
    response = requests.delete(f"{API_URL}/properties/{delete_id}")

    if response.status_code == 200:
        st.success("Deleted successfully")
    else:
        st.error("Error deleting property")