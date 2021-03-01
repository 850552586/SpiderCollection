# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YgzwItem(scrapy.Item):
    #标题
    title = scrapy.Field()
    #日期
    date = scrapy.Field()
    #发布人
    author = scrapy.Field()
    #通知内容
    content = scrapy.Field()