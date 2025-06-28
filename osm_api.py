# data_analysis/pipeline/osm_api.py

import requests

def fetch_osm_data(store_name, country='Canada'):
    """
    Fetches store data from OpenStreetMap using the Nominatim API.
    Args:
        store_name (str): Name of the store to search.
        country (str): Country scope (default: Canada).
    Returns:
        list: Store information dictionaries.
    """
    nominatim_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{store_name}, {country}",
        "format": "json",
        "limit": 10000
    }

    headers = {"User-Agent": "MyOSMApp/1.0"}
    try:
        response = requests.get(nominatim_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data:
            parts = item['display_name'].split(", ")
            name = parts[0] if parts else store_name
            address = " ".join(parts[1:-3])
            city = parts[-4] if len(parts) >= 4 else ""
            province = parts[-3] if len(parts) >= 3 else ""
            postal_code = parts[-2] if len(parts) >= 2 else ""
            country = parts[-1] if parts else "Canada"

            results.append({
                "Name": name,
                "Address": address,
                "City": city,
                "Province": province,
                "Country": country,
                "Postal Code": postal_code,
                "Category": item.get("type", ""),
                "Logo": item.get("icon", ""),
                "Latitude": item.get("lat", 0.00),
                "Longitude": item.get("lon", 0.00),
                "CardLoyaltyProgram": "",
                "BrandName": "",
                "BankName": "",
                "CardTypeName": "",
                "email": "",
                "cellNum": ""
            })
        return results

    except requests.exceptions.RequestException as e:
        print(f"[OSM ERROR] {store_name}: {e}")
        return []
