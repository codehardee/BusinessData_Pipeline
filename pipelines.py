class StoreLogoPipeline:
    logo_data = []

    @classmethod
    def process_item(cls, item, spider):
        cls.logo_data.append({
            'store_name': item.get('store_name', 'Unknown Store'),
            'favicon_url': item.get('favicon_url', ''),
            'saved_favicon_path': item.get('saved_favicon_path', '')
        })
        return item
