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


class GithubProjectItem(scrapy.Item):
    url = scrapy.Field()
    watch = scrapy.Field()
    star = scrapy.Field()
    fork = scrapy.Field()

    commits = scrapy.Field()
    commitsLink = scrapy.Field()
    commitHistory = scrapy.Field()

    branches = scrapy.Field()
    packages = scrapy.Field()
    releases = scrapy.Field()
    contributors = scrapy.Field()
    license = scrapy.Field()

    about = scrapy.Field()
    readme = scrapy.Field()



class QuoteItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
