# data_analysis/pipeline/here_api.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
HERE_API_KEY = os.getenv("HERE_API_KEY")

if not HERE_API_KEY:
    raise ValueError("API Key not found. Set HERE API in .env file.")

def get_store_details_here(store_name, latitude, longitude):
    """
    Fetches store data using HERE API based on coordinates.
    Args:
        store_name (str): Name of the store.
        latitude (float): Latitude of the city.
        longitude (float): Longitude of the city.
    Returns:
        list: Store information dictionaries.
    """
    url = f"https://discover.search.hereapi.com/v1/discover?apikey={HERE_API_KEY}&q={store_name}&at={latitude},{longitude}&limit=5"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        stores = []
        for item in data.get("items", []):
            website = "N/A"
            if "contacts" in item:
                for contact in item["contacts"]:
                    if contact.get("www"):
                        website = contact["www"][0].get("value", "N/A")
                        break

            stores.append({
                "Name": item.get("title", ""),
                "Address": item.get("address", {}).get("label", ""),
                "City": item.get("address", {}).get("city", ""),
                "Province": item.get("address", {}).get("state", ""),
                "Country": item.get("address", {}).get("countryCode", "CA"),
                "Postal Code": item.get("address", {}).get("postalCode", ""),
                "Logo": item.get("icon", ""),
                "Website": website,
                "Latitude": item.get("position", {}).get("lat", 0.00),
                "Longitude": item.get("position", {}).get("lng", 0.00),
                "Category": item.get("resultType", ""),
                "CardLoyaltyProgram": "",
                "BrandName": "",
                "BankName": "",
                "CardTypeName": "",
                "email": "",
                "cellNum": item.get("contacts", [{}])[0].get('phone', [{}])[0].get('value', "")
            })
        return stores

    except requests.exceptions.RequestException as e:
        print(f"[HERE API ERROR] {store_name}: {e}")
        return []
