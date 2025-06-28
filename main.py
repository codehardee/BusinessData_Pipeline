import pandas as pd
from pipeline.osm_api import fetch_osm_data
from pipeline.here_api import get_store_details_here
# from pipeline.anthropic_api import fetch_official_website
from pipeline.logo_scraper import fetch_logo

from pipeline.store_url_map import store_url_map




def normalize_fields(store):
    return (
        str(store.get("Address", "")).strip().lower(),
        str(store.get("City", "")).strip().lower()
)


def merge_store_data(osm_data, here_data):
    merged_data = osm_data.copy()
    osm_keys = {normalize_fields(store) for store in osm_data}

    for store in here_data:
        if normalize_fields(store) not in osm_keys:
            merged_data.append(store)

    return merged_data


def enrich_with_logo_and_website(merged_data):
    for store in merged_data:
        name = store.get("Name", "")
        url = store_url_map.get(name, "")
        store["Website"] = url

        print("storename is this", name, "url is this", url, "store is this", store)

        # logo_info_list = fetch_logo({name: url})
        # if logo_info_list and isinstance(logo_info_list, list):
        #     info_dict = logo_info_list[0].get(name, ["", ""])
        #     store["Favicon URL"] = info_dict[0]
        #     store["Favicon Path"] = info_dict[1]
        # else:
        #     store["Favicon URL"] = ""
        #     store["Favicon Path"] = ""
        print("in the main , trying to get url....", url)
        logo_info_map = fetch_logo({name: url})
        print("logo info map", logo_info_map)

        info_dict = logo_info_map.get(name, {})
        print("dictionary information!!!!!!!!!!!!!!!!!", info_dict)

        store["Favicon URL"] = info_dict.get("favicon_url", "")
        store["Favicon Path"] = info_dict.get("saved_favicon_path", "")

        store["Base64 Logo"] = ""
    return merged_data




def save_to_excel(data, filename="store_data.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")


def main(store_name):
    print(f"Collecting data for: {store_name}")
    osm_data = fetch_osm_data(store_name)

    # print("osm data from osm!!!!!!!!!!!!!!!", osm_data)

    province_coordinates = [
        {"city": "Toronto", "lat": 43.7001, "lng": -79.4163},
        {"city": "Vancouver", "lat": 49.2827, "lng": -123.1207},
        {"city": "Montreal", "lat": 45.5017, "lng": -73.5673},
        {"city": "Calgary", "lat": 51.0447, "lng": -114.0719},
        {"city": "Edmonton", "lat": 53.5461, "lng": -113.4938},
        {"city": "Ottawa", "lat": 45.4215, "lng": -75.6993},
        {"city": "Winnipeg", "lat": 49.8951, "lng": -97.1384},
        {"city": "Quebec City", "lat": 46.8139, "lng": -71.2082},
        {"city": "Hamilton", "lat": 43.2557, "lng": -79.8711},
        {"city": "Halifax", "lat": 44.6488, "lng": -63.5752},
        {"city": "Victoria", "lat": 48.4284, "lng": -123.3656},
        {"city": "Saskatoon", "lat": 52.1579, "lng": -106.6702},
        {"city": "Regina", "lat": 50.4452, "lng": -104.6189},
        {"city": "St. John's", "lat": 47.5615, "lng": -52.7126},
        {"city": "London", "lat": 42.9849, "lng": -81.2453},
        {"city": "Windsor", "lat": 42.3149, "lng": -83.0364},
        {"city": "Kitchener", "lat": 43.4516, "lng": -80.4925},
        {"city": "Kelowna", "lat": 49.8872, "lng": -119.4961},
        {"city": "Barrie", "lat": 44.3894, "lng": -79.6903},
        {"city": "Sherbrooke", "lat": 45.4000, "lng": -71.8991},
        {"city": "Guelph", "lat": 43.5448, "lng": -80.2482},
        {"city": "Trois-RiviÃ¨res", "lat": 46.3491, "lng": -72.5497},
        {"city": "Saint John", "lat": 45.2733, "lng": -66.0633},
        {"city": "Thunder Bay", "lat": 48.3809, "lng": -89.2477},
        {"city": "Moncton", "lat": 46.0878, "lng": -64.7782}
    ]

    here_data = []
    for location in province_coordinates:
        results = get_store_details_here(store_name, location["lat"], location["lng"])
        here_data.extend(results)

    # print("here data from here!!!!!!", here_data)

    # here_data = get_store_details_here(store_name)
    merged_data = merge_store_data(osm_data, here_data)

    # print("merged data of osm and here!!!!!!!!", merged_data)

    enriched_data = enrich_with_logo_and_website(merged_data)

    print("enriched data!!!!!!!!!", enriched_data)
    save_to_excel(enriched_data)


if __name__ == "__main__":
    for store_name in store_url_map.keys():
        try:
            main(store_name)
        except Exception as e:
            import traceback

            print(f"Failed for {store_name}: {e}")
            traceback.print_exc()

