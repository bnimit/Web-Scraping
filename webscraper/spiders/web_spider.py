import scrapy
from urllib.parse import urlparse

class WebSpiderSpider(scrapy.Spider):
    name = "web_spider"
    start_urls = []
    allowed_domains = []
    
    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as f:
                for url in f.readlines():
                    self.start_urls.append(url.strip())
                    self.allowed_domains.append(urlparse(url).netloc)


    def parse(self, response):
        business_type = ''
        og_type = response.css('meta[property="og:type"]::attr(content)').get()
        meta_type = response.css('meta[name="type"]::attr(content)').get()
        description = response.css('meta[name="description"]::attr(content)').get()

        if(og_type == 'article' or meta_type == 'article' or response.css('div.article')):
               business_type = 'blog' if 'blog' in response.url else 'news'                 
        elif response.css('div.product') or any(ele in response.text for ele in ['price', 'returns', 'delivery']):
            business_type = "e-commerce"
        else:
            business_type = 'Unknown'

        yield {
            'og_type': og_type,
            'type': meta_type,
            'business': business_type,
            'description': description
        }

