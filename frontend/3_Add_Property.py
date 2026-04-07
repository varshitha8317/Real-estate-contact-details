import streamlit as st
import sys
import os

# allow Streamlit pages to access root folder
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api_client import get_cities, get_areas, add_property


st.title("Add Property")

# load cities
cities = get_cities()

if not cities:
    st.error("Backend API not running")
    st.stop()

# dropdowns
city = st.selectbox("City", cities)

areas = get_areas(city)

area = st.selectbox("Area", areas)


# form
with st.form("property_form"):

    title = st.text_input("Property Title")

    price = st.number_input(
        "Price",
        min_value=0
    )

    description = st.text_area(
        "Description"
    )

    submit = st.form_submit_button(
        "Submit Property"
    )


if submit:

    success = add_property(
        city,
        area,
        title,
        price,
        description
    )

    if success:
        st.success("Property added successfully")

    else:
        st.error("Failed to add property")