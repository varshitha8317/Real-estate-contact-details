import streamlit as st
from api_client import get_cities, get_areas, get_properties

st.header("Chat Assistant")

# store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# dropdowns
col1, col2 = st.columns(2)

with col1:
    city = st.selectbox(
        "Select City",
        get_cities(),
        key="chat_city"
    )

with col2:
    area = st.selectbox(
        "Select Area",
        get_areas(city),
        key="chat_area"
    )

# search button
if st.button("Search Properties"):

    # user message
    user_msg = f"Show properties in {city}, {area}"

    st.session_state.messages.append({
        "role": "user",
        "content": user_msg
    })

    properties = get_properties(city, area)

    # assistant response
    if len(properties) == 0:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "No properties found"
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"{len(properties)} properties found"
        })

        for p in properties:
            st.session_state.messages.append({
                "role": "assistant",
                "content":
                f"""
🏠 {p['title']}
📍 {p['area']}, {p['city']}
💰 ₹{p['price']}
"""
            })

# display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])