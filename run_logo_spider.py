
import sys
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pipeline.pipelines import StoreLogoPipeline
from pipeline.spiders.logo_spider import LogoSpider

def run_spider(store_name, url):
    store_url_map = {store_name: url}

    process = CrawlerProcess(settings={
        **get_project_settings(),
        'LOG_ENABLED': False,
        'ITEM_PIPELINES': {'pipeline.pipelines.StoreLogoPipeline': 1}
    })

    StoreLogoPipeline.logo_data = []
    process.crawl(LogoSpider, store_url_map=store_url_map)
    process.start()

    if StoreLogoPipeline.logo_data:
        entry = StoreLogoPipeline.logo_data[0]
        result = {
            'store_name': entry['store_name'],
            'favicon_url': entry.get('favicon_url', ''),
            'saved_favicon_path': entry.get('saved_favicon_path', '')
        }
        print(json.dumps(result))  # Send to stdout

if __name__ == "__main__":
    store_name = sys.argv[1]
    url = sys.argv[2]
    run_spider(store_name, url)
