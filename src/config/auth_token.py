import requests
from src.config.config import BASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD

def get_token():
    url = f"{BASE_URL}/api/v2/admin/administrators/token"
    payload = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }

    response = requests.post(url, json=payload)
    return response.json()["token"]