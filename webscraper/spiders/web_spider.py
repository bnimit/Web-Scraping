import scrapy
import json
import os
from urllib.parse import urlparse

class WebSpiderSpider(scrapy.Spider):
    base_path = os.getcwd() + '/output'
    name = "web_spider"
    start_urls = []
    allowed_domains = []
    unique_links = set()
    
    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as f:
                for url in f.readlines():
                    self.unique_links.add(url.strip())

        self.start_urls = list(self.unique_links)
        for url in self.start_urls:
            self.allowed_domains.append(urlparse(url).netloc)

    def parse(self, response):
        business_type = ''
        og_type = response.css('meta[property="og:type"]::attr(content)').get()
        meta_type = response.css('meta[name="type"]::attr(content)').get()
        description = response.css('meta[name="description"]::attr(content)').get()
        title = response.css('title::text').get()

        # identify the type of webpage, news, e-commerce etc.
        if(og_type == 'article' or meta_type == 'article' or response.css('div.article')):
            business_type = 'blog' if 'blog' in response.url else 'news'  
            author = response.css('meta[name="author"]::attr(content)').get()
            publisher = response.css('meta[property="article:publisher"]::attr(content)').get()
            news_object = {
                'title': title,
                'category': business_type,
                'author': author,
                'publisher': publisher,
                'description': description
            }
            with open(self.base_path+'/news.json', 'w') as jsonfile:
                jsonfile.write(json.dumps(news_object, indent=4))


        # If the page is related to e-commerce do further processing ( customized for Amazon only currently)
        elif response.css('div.product') or any(ele in response.text for ele in ['price', 'returns', 'delivery']):
            business_type = "e-commerce"   
            if title.startswith('Amazon'):
                yield response.follow(response.url, callback=self.parse_amazon_product)
        else:
            # if the type is unknown
            business_type = 'Unknown'
            unknown_object = {
            'og_type': og_type,
            'type': meta_type,
            'category': business_type,
            'description': description
            }
            
            with open(self.base_path+'/unknown.json', 'w') as jsonfile:
                json.dump(unknown_object, jsonfile)

    def parse_amazon_product(self, response):
        amazon_object = {
            'title': response.css('span#productTitle::text').get().strip(),
            'category': response.xpath("//li[@class='a-breadcrumb-divider'][last()]/following::li[1]//span//a/text()").get().strip(),
            'price': "$"+ ''.join(response.xpath("//span[@class='a-price-whole']/text()")[1].get().strip()),
            'main_category': response.xpath("//li[@class='a-breadcrumb-divider'][last()]/preceding-sibling::li[1]//span//a/text()").get().strip(),
            'rating': response.xpath("//span[@class='a-icon-alt']/text()")[2].extract()
        }
        print('AMAZONOBJECT:->', amazon_object)
        with open(self.base_path+'/amazon_products.json', 'w') as jsonfile:
            json.dump(amazon_object, jsonfile)