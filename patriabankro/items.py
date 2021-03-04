import scrapy


class PatriabankroItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
