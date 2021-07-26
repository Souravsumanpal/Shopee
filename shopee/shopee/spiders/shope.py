import scrapy
import json



class ShopeSpider(scrapy.Spider):
    name = 'shope'
    # allowed_domains = ['abc.com']
    start_urls = ['https://shopee.com.my/Women-Clothes-cat.11000538']

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://shopee.com.my/Women-Clothes-cat.11000538",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    def start_requests(self):
        
        for item in range(0,6000,60):
            url = f"https://shopee.com.my/api/v4/search/search_items?by=relevancy&limit=100&match_id=11000538&newest={item}&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2"
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
            

    def parse(self, response):
        url = 'https://shopee.com.my/api/v4/product/get_shop_info?shopid='
        raw = response.body
        data = json.loads(raw)
        for shop in data['items']:
            shop_id = shop['item_basic']['shopid']
            final_url = url + str(shop_id)
            yield scrapy.Request(url=final_url, callback=self.parseapi, headers=self.headers)

    
    def parseapi(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        yield{
            'Shop_name': data['data']['name'],
            'Products': data['data']['item_count'],
            'Chart_Performance': data['data']['response_rate'],
            'Rating': data['data']['rating_star'],
            'Followers': data['data']['follower_count'],
            'Rating_bad': data['data']['rating_bad'],
            'Rating_good': data['data']['rating_good'],
            'Rating_normal': data['data']['rating_normal'],
        }        

