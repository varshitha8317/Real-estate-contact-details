import requests

BASE_URL = "http://localhost:8000"

def get_cities():
    try:
        res = requests.get(f"{BASE_URL}/cities")
        return res.json()
    except:
        return []

def get_areas(city):
    try:
        res = requests.get(
            f"{BASE_URL}/areas",
            params={"city": city}
        )
        return res.json()
    except:
        return []

def add_property(city, area, title, price, description):

    data = {
        "city": city,
        "area": area,
        "title": title,
        "price": price,
        "description": description
    }

    try:
        res = requests.post(
            f"{BASE_URL}/properties",
            json=data
        )

        return res.status_code in [200,201]

    except:
        return False