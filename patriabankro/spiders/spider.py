import scrapy

from scrapy.loader import ItemLoader
from ..items import PatriabankroItem
from itemloaders.processors import TakeFirst


class PatriabankroSpider(scrapy.Spider):
	name = 'patriabankro'
	start_urls = ['https://www.patriabank.ro/despre-patria/informatii-presa/comunicate-de-presa']

	def parse(self, response):
		post_links = response.xpath('//article/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="summary"]//text()[normalize-space()]|//div[@class="page"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=PatriabankroItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
