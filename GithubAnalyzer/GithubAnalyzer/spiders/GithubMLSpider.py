# -*- coding: utf-8 -*-
import scrapy
from ..items import GithubItem
import time

class GithubMLSpider(scrapy.Spider):
    name = 'GithubML'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/search?p=1&q=machine+learning&type=Repositories']
    pageNumber = 1

    baseurl = 'https://github.com/'

    def parse(self, response):
        repoClass = "repo-list-item d-flex flex-column flex-md-row flex-justify-start py-4 public source"
        repoList = response.xpath('//ul[@class = "repo-list"]')
        items = GithubItem()
        #for repo in response.xpath('//li[@class = ' + repoClass+']'):
        for repo in repoList.xpath('./li'):
            items['url'] = self.baseurl + repo.xpath('.//a[@class = "v-align-middle"]/@href').extract_first()
            yield items
        self.pageNumber += 1

        nextPage = 'https://github.com/search?p=' + str(self.pageNumber) + '&q=machine+learning&type=Repositories'
        #nextPage = response.xpath('.//a[@rel="next"]/@href').get()
        print ('Page: ' + str(self.pageNumber))
        time.sleep(1)
        if self.pageNumber <= 100:
            yield response.follow(nextPage, callback=self.parse)
