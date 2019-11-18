# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class GithubItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    language = scrapy.Field()


class GithubProjectItem(scrapy.item):
    watch = scrapy.Field()
    star = scrapy.Field()
    fork = scrapy.Field()




class QuoteItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()