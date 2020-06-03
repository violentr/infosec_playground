import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(scrapy.Spider):
	name = 'jokes'
	allowed_domains = ['laughfactory.com']
	start_urls = ['http://laughfactory.com/jokes/family-jokes']


	def parse(self, response):
	    for joke in response.xpath("//div[@class='jokes']"):
	        yield { "joke" : joke.xpath(".//div[@class='joke-text']/p").extract_first() }
	    next_page = response.xpath("//li[@class='next']/a/@href").extract_first()
	    if next_page is not None:
	        next_page_link = response.urljoin(next_page)
	        yield scrapy.Request(url=next_page_link, callback=self.parse)
