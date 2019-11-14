# -*- coding: utf-8 -*-
import scrapy
from ..items import GithubItem
import time


class GithubLinksSpider(scrapy.Spider):
    name = 'GithubLinksSpider'
    allowed_domains = ['github.com']
    start_urls = [
        'https://github.com/search?o=desc&q=machine+learning&s=updated&type=Repositories',
        'https://github.com/search?l=Python&o=desc&q=machine+learning&s=updated&type=Repositories',
        'https://github.com/search?l=Jupyter+Notebook&o=desc&q=machine+learning&s=updated&type=Repositories',
        'https://github.com/search?l=Java&o=desc&q=machine+learning&s=updated&type=Repositories',
        'https://github.com/search?l=JavaScript&o=desc&q=machine+learning&s=updated&type=Repositories'
    ]
    pageNumber = 1
    urlID = 1

    baseurl = 'https://github.com/'

    def parse(self, response):
        repoList = response.xpath('//ul[@class = "repo-list"]')
        repos = repoList.xpath('./li')
        items = GithubItem()
        for repo in repos:
            items['url'] = self.baseurl + repo.xpath('.//a[@class = "v-align-middle"]/@href').extract_first()
            items['id'] = self.urlID
            yield items


        #nextPage = 'https://github.com/search?p=' + str(self.pageNumber) + '&q=machine+learning&type=Repositories'
        nextPage = response.xpath('//a[@rel = "next"]/@href').extract_first()

        if nextPage:
            self.pageNumber += 1
            print ('Page: ' + str(self.pageNumber))

            yield response.follow(self.baseurl + nextPage, callback=self.parse)
        else:
            self.urlID += 1
