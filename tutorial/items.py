import scrapy


class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    time = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    articleid=scrapy.Field()
    pass
