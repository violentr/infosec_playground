import scrapy, re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from jokes.items import JokesItem
from scrapy.loader import ItemLoader
from urllib.parse import urlparse

class MySpider(scrapy.Spider):
    name = 'jokes'
    allowed_domains = ['laughfactory.com']
    start_urls = ['http://laughfactory.com/jokes/family-jokes']

    def parse(self, response):
        for joke in response.xpath("//div[@class='jokes']"):
            l = ItemLoader(item=JokesItem(),selector=joke)
            l.add_xpath("joke_text",".//div[@class='joke-text']/p")
            yield l.load_item()

        next_page = response.xpath("//li[@class='next']/a/@href").extract_first()
        scheme = urlparse(next_page).scheme
        if re.search("http|https", scheme) is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
