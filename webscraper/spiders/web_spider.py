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
            title = response.css('title::text').get()
            if title.startswith('Amazon'):
                yield response.follow(response.url, callback=self.parse_amazon_product)
        else:
            business_type = 'Unknown'

        yield {
            'og_type': og_type,
            'type': meta_type,
            'category': business_type,
            'description': description
        }

    def parse_amazon_product(self, response):
        yield {
            'title': ' '.join(response.css('span#productTitle::text').get().split()),
            'category': ' '.join(response.xpath("//li[@class='a-breadcrumb-divider'][last()]/following::li[1]//span//a/text()").get().split()),
            'main_category': ' '.join(response.xpath("//li[@class='a-breadcrumb-divider'][last()]/preceding-sibling::li[1]//span//a/text()").get().split()),
            'product_rating': response.xpath("//span[@class='a-icon-alt']/text()")[2].extract()
        }

