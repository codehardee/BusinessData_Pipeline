import scrapy
import os
import mimetypes
from urllib.parse import urlparse


class LogoSpider(scrapy.Spider):
    name = 'logo_spider'

    def __init__(self, store_url_map=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.store_url_map = store_url_map or {}
        # self.start_urls = list(self.store_url_map.values())
        if not isinstance(store_url_map, dict):
            raise ValueError("store_url_map must be a dictionary {store_name: url}")
        self.store_url_map = store_url_map
        self.start_urls = list(store_url_map.values())

    def start_requests(self):
        for url in self.start_urls:
            store_name = next((k for k, v in self.store_url_map.items() if v == url), "Unknown Store")
            yield scrapy.Request(url, callback=self.parse, meta={'store_name': store_name})

    def parse(self, response):
        store_name = response.meta.get('store_name', 'Unknown Store')
        favicon_urls = response.xpath("//link[contains(@rel, 'icon')]/@href").getall()

        if not favicon_urls:
            favicon_urls = [response.urljoin('/favicon.ico')]
        else:
            favicon_urls = [response.urljoin(url) for url in favicon_urls]

        if favicon_urls:
            yield scrapy.Request(
                url=favicon_urls[0],
                callback=self.save_favicon,
                meta={
                    'store_name': store_name,
                    'favicon_url': response.url
                },
                dont_filter=True
            )

    def save_favicon(self, response):
        folder_path = 'logo'
        os.makedirs(folder_path, exist_ok=True)

        store_name = response.meta.get('store_name', 'Unknown Store')
        source_domain = response.meta.get('favicon_url', '')

        domain = urlparse(source_domain).netloc.replace(".", "_")
        content_type = response.headers.get('Content-Type', b'').decode()
        ext = mimetypes.guess_extension(content_type) or ".ico"
        filename = f"{domain}_favicon{ext}"
        filepath = os.path.join(folder_path, filename)

        if not os.path.exists(filepath):
            with open(filepath, 'wb') as f:
                f.write(response.body)

        yield {
            'store_name': store_name,
            'favicon_url': source_domain,
            'saved_favicon_path': filepath
        }
