import scrapy

from scrapy.loader import ItemLoader
from ..items import BankfrickItem
from itemloaders.processors import TakeFirst


class BankfrickSpider(scrapy.Spider):
	name = 'bankfrick'
	start_urls = ['https://www.bankfrick.li/de/ueber-bank-frick/medien']

	def parse(self, response):
		page_links = response.xpath('//div[@class="article_pager"]/a/@href').getall()
		yield from response.follow_all(page_links, self.parse_page)

	def parse_page(self, response):
		post_links = response.xpath('//div[@class="edn_463_article_list_wrapper"]/article/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		print(response)
		title = response.xpath('//h1/text()').get()
		print(title)
		description = response.xpath('//article//p//text()[normalize-space() and not(ancestor::div[@class="subinfos"])]|//article//h2//text()').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="datebox"]/span/text()').getall()
		date = ' '.join(date).strip()

		item = ItemLoader(item=BankfrickItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
