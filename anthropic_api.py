import anthropic
import re
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")

class AnthropicWebsiteFetcher:
    def __init__(self, api_key=None):
        self.api_key = API_KEY
        if not self.api_key:
            raise ValueError("Anthropic API key must be provided or set in the environment as ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def fetch_official_website(self, store_name: str) -> str:
        """
        Fetches the official website URL for the given store name using Claude (Anthropic API).

        Args:
            store_name (str): The name of the store.

        Returns:
            str: The official website URL or None if not found.
        """
        query = f"What is the official website of {store_name}?"

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": query}]
            )

            website_text = response.content[0].text.strip()

            match = re.search(
                r'\b(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.(?:com|ca)\b',
                website_text
            )

            if match:
                url = match.group(0)
                return f"https://{url}" if not url.startswith('http') else url
            return None

        except Exception as e:
            print(f"Error fetching website from Anthropic: {e}")
            return None

fetcher_instance = AnthropicWebsiteFetcher()

def fetch_official_website(store_name: str) -> str:
    return fetcher_instance.fetch_official_website(store_name)
