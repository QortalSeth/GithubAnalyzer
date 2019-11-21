import scrapy
from ..items import QuoteItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        items = QuoteItem()
       # title = response.xpath('//title/text()').extract_first()
        divQuotes = response.xpath('//div[@class = "quote"]')
        for quoteDiv in divQuotes:
            quote = quoteDiv.xpath('.//span[@class = "text"]/text()').extract_first()
            author = quoteDiv.xpath('.//small[@class = "author"]/text()').extract()
            tags = quoteDiv.xpath('.//a[@class = "tag"]/text()').extract()

            items['quote'] = quote
            items['author'] = author
            items['tags'] = tags
            yield items
        nextPage = response.xpath('//li[@class = "next"]/a/@href').get()

        if nextPage is not None:
            yield response.follow(nextPage, self.parse)


