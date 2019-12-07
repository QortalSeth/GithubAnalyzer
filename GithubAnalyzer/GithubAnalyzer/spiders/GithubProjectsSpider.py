# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from ..items import GithubProjectItem
import re
import traceback
import csv

class GithubProjectsSpider(scrapy.Spider):
    name = 'GithubProjectsSpider'
    allowed_domains = ['github.com']
    links = pd.read_csv('urlsDebugProcessed.csv')
    #start_urls = ['https://github.com/josephmisiti/awesome-machine-learning']
    start_urls = links.loc[links['id'] == -1, 'url'].tolist()
    baseurl = 'https://github.com/'

    failedUrls = {}
    custom_settings = {
        'ITEM_PIPELINES': {'GithubAnalyzer.pipelines.LinksPipeline': 300}
    }

    def executeScrape(self, function, response, item):
        try:
            return function(response, item)
        except:
            track = traceback.format_exc()
            print(track)
            self.failedUrls[response.request.url] = track
            return item

    def parsePageHead(self, response, item):
        pageHead = response.xpath('//ul[@class="pagehead-actions"]')

        listLen = len(pageHead.xpath('./li'))
        index = 1


        if listLen > 3:
            index += 1

        watch = pageHead.xpath('./li[ '+ str(index) +']/a[2]/@aria-label').extract_first()

        print('Index is: ' + str(index))
        print('Watch is: ' + watch)
        item['watch'] = re.sub("[^\d]", "", watch)
        listLen += 1
        item['star'] = re.sub("[^\d]", "", pageHead.xpath('./li['+ str(index) +']/a[2]/@aria-label').extract_first())
        listLen += 1
        item['fork'] = re.sub("[^\d]", "", pageHead.xpath('./li['+str(index)+']/a[2]/@aria-label').extract_first())

        about = response.xpath('//span[@itemprop="about"]/text()').extract_first()
        if about is not None:
            item['about'] = about.strip()

        return item

    def parseNumbersSummary(self, response, item):
        numSummary = response.xpath("//ul[@class='numbers-summary']")
        listLen = len(numSummary.xpath('./li'))
        # print ('commits: '+ str(numSummary.xpath("./li[1]").extract_first()))
        commitsLink = numSummary.xpath("./li[1]/a/@href").extract_first()
        if commitsLink is not None:
            item['commitsLink']  = self.baseurl + commitsLink
        commits = numSummary.xpath("./li[1]//span/text()").extract_first()
        if commits is None:
            item['contributors'] = -2
            return item
        item['commits']      = re.sub("[^\d]", "", commits)
        item['branches']     = re.sub("[^\d]", "", numSummary.xpath("./li[2]//span/text()").extract_first())
        item['packages']     = re.sub("[^\d]", "", numSummary.xpath("./li[3]//span/text()").extract_first())
        item['releases']     = re.sub("[^\d]", "", numSummary.xpath("./li[4]//span/text()").extract_first())

        contributors = numSummary.xpath("./li[5]//span/text()").extract_first()
        if contributors is None:
            item['contributors'] = -1
        else:
            item['contributors'] = re.sub("[^\d]", "", contributors)

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
        readmeLink = response.xpath('//a[@title="README.md"]/@href').get()

        if readmeLink is not None:
            return response.follow(self.baseurl + readmeLink, callback=self.parseReadme2, meta={'item': item})

    def parseReadme2(self, response):
        item = response.meta['item']
        rawReadmeLink = self.baseurl + response.xpath('//a[@id="raw-url"]/@href').extract_first()
        return response.follow(rawReadmeLink, callback=self.parseReadmeFinal, meta={'item': item})

    def parseReadmeFinal(self, response):
        item = response.meta['item']
        text = ''.join(response.xpath('//body//text()').extract())
        item['readme'] = text
        return item




    def parse(self, response):
        url = response.request.url
        item = GithubProjectItem()
        item['url'] = url


        item = self.executeScrape(self.parseNumbersSummary, response, item)
        if item['contributors'] < 0:
            self.links.loc[self.links['url'] == url, 'id'] = -2
            print 'url: ' + url +'has no commits'
            yield None

        item = self.executeScrape( self.parsePageHead,response, item)
        item = self.executeScrape(self.parseReadme,response, item)

        self.links.loc[self.links['url'] == url, 'id'] = 1
        yield item

    def closed( self, reason ):
        self.links.to_csv('urlsDebugProcessed.csv', index=False)
        (pd.DataFrame.from_dict(data=self.failedUrls, orient='index')
         .to_csv('FailedURLs.csv'))



