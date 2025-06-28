
import subprocess
import json
import sys

def fetch_logo(store_url_map):
    if not store_url_map:
        return {}

    store_name, url = list(store_url_map.items())[0]

    try:
        result = subprocess.run(
            [sys.executable, "pipeline/run_logo_spider.py", store_name, url],
            capture_output=True,
            text=True,
            check=True
        )

        if result.stdout:
            data = json.loads(result.stdout)
            return {
                data['store_name']: {
                    'favicon_url': data.get('favicon_url', ''),
                    'saved_favicon_path': data.get('saved_favicon_path', '')
                }
            }
    except Exception as e:
        print(f"Error running logo scraper subprocess: {e}")

    return {}
