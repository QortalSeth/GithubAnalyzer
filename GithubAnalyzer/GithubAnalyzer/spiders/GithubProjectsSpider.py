# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from ..items import GithubProjectItem
import re


class GithubProjectsSpider(scrapy.Spider):
    name = 'GithubProjectsSpider'
    allowed_domains = ['www.github.com']
    links = pd.read_csv('urlsDebug.csv')
    start_urls = ['https://github.com/josephmisiti/awesome-machine-learning']

    custom_settings = {
        'ITEM_PIPELINES': {'GithubAnalyzer.pipelines.LinksPipeline': 300}
    }

    def parsePageHead(self, response, item):
        pageHead = response.xpath('//ul[@class="pagehead-actions"]')
        item['watch'] = re.sub("[^\d]", "", pageHead.xpath('./li[1]/a[2]/@aria-label').extract_first())
        item['star'] = re.sub("[^\d]", "", pageHead.xpath('./li[2]/a[2]/@aria-label').extract_first())
        item['fork'] = re.sub("[^\d]", "", pageHead.xpath('./li[3]/a[2]/@aria-label').extract_first())
        return item

    def parseNumbersSummary(self, response, item):
        numSummary = response.xpath("//ul[@class='numbers-summary']")

        print ('commits: '+ str(numSummary.xpath("./li[1]").extract_first()))
        item['commits'] = re.sub("[^\d]", "", numSummary.xpath("./li[1]//span[@class='num text-emphasized']/text()").extract_first())
        item['branches'] = re.sub("[^\d]", "", numSummary.xpath("./li[2]//span[@class='num text-emphasized']/text()").extract_first())
        item['packages'] = re.sub("[^\d]", "", numSummary.xpath("./li[3]//span[@class='num text-emphasized']/text()").extract_first())
        item['releases'] = re.sub("[^\d]", "", numSummary.xpath("./li[4]//span[@class='num text-emphasized']/text()").extract_first())
        item['contributors'] = re.sub("[^\d]", "", numSummary.xpath("./li[5]//span[@class='num text-emphasized']/text()").extract_first())

        listLen = len(numSummary.xpath('./li'))
        if listLen == 6:
            item['license'] = numSummary.xpath("./li[6]/a").extract_first()
        else:
            item['license'] = 'No License'
        return item

    def parse(self, response):
        item = GithubProjectItem()
        item['url'] = response.request.url
        item = self.parsePageHead(response, item)
        item = self.parseNumbersSummary(response,item)

        yield item
    #      print (link)
    #   links = links.drop_duplicates(subset = 'url', keep='first')
    #   links = links['url']
    #   links.to_csv('urlsDebug.csv')
