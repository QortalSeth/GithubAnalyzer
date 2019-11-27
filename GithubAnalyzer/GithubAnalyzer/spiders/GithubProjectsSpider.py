# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from ..items import GithubProjectItem
import re


class GithubProjectsSpider(scrapy.Spider):
    name = 'GithubProjectsSpider'
    allowed_domains = ['https://github.com']
    links = pd.read_csv('urlsDebug.csv')
    start_urls = ['https://github.com/josephmisiti/awesome-machine-learning']
    baseurl = 'https://github.com/'

    custom_settings = {
        'ITEM_PIPELINES': {'GithubAnalyzer.pipelines.LinksPipeline': 300}
    }

    def parsePageHead(self, response, item):
        pageHead = response.xpath('//ul[@class="pagehead-actions"]')
        item['watch'] = re.sub("[^\d]", "", pageHead.xpath('./li[1]/a[2]/@aria-label').extract_first())
        item['star'] = re.sub("[^\d]", "", pageHead.xpath('./li[2]/a[2]/@aria-label').extract_first())
        item['fork'] = re.sub("[^\d]", "", pageHead.xpath('./li[3]/a[2]/@aria-label').extract_first())
        item['about'] = response.xpath('//span[@itemprop="about"]/text()').extract_first().strip()
        return item

    def parseNumbersSummary(self, response, item):
        numSummary = response.xpath("//ul[@class='numbers-summary']")
        listLen = len(numSummary.xpath('./li'))
        # print ('commits: '+ str(numSummary.xpath("./li[1]").extract_first()))
        item['commitsLink'] =  self.baseurl + numSummary.xpath("./li[1]/a/@href").extract_first()
        item['commits']      = re.sub("[^\d]", "", numSummary.xpath("./li[1]//span/text()").extract_first().strip())
        item['branches']     = re.sub("[^\d]", "", numSummary.xpath("./li[2]//span/text()").extract_first().strip())
        item['packages']     = re.sub("[^\d]", "", numSummary.xpath("./li[3]//span/text()").extract_first().strip())
        item['releases']     = re.sub("[^\d]", "", numSummary.xpath("./li[4]//span/text()").extract_first().strip())
        item['contributors'] = re.sub("[^\d]", "", numSummary.xpath("./li[5]//span/text()").extract_first().strip())

        if listLen == 6:
            license = numSummary.xpath("./li[6]/a/text()").extract()[1].strip().lower()

            if license == 'view license':
                item['license'] = 'Custom'
            else:
                item['license'] = license
        else:
            item['license'] = 'No License'
        return item

    def parseReadme(self, response, item):
        readmeLink = self.baseurl + response.xpath('//a[@title="README.md"]/@href').get()

        if readmeLink is not None:
            response.follow(readmeLink, callback=self.parseReadme2, meta={'item': item})

            #x = response.follow(readmeLink)
            #nextResponse = x.response()

    def parseReadme2(self, response):
        item = response.meta['item']
        rawReadmeLink = self.baseurl + response.xpath('//a[@id="raw-url"]/@href').extract_first()
        rawReadmeLink = response.urljoin(rawReadmeLink)
        yield response.follow(rawReadmeLink, callback=self.parseReadmeFinal, meta={'item': item})

    def parseReadmeFinal(self, response):
        item = response.meta['item']
        item['readme'] = response.xpath('//pre/text()').extract_first()
        return item

 #   def parseCommitHistory(self, response, item):
 #       yield item

    def parse(self, response):
        item = GithubProjectItem()
        item['url'] = response.request.url
        item = self.parsePageHead(response, item)
        item = self.parseNumbersSummary(response, item)
        item = self.parseReadme(response, item)
#        item = self.parseCommitHistory(response,item)
        return item
    #      print (link)
    #   links = links.drop_duplicates(subset = 'url', keep='first')
    #   links = links['url']
    #   links.to_csv('urlsDebug.csv')
