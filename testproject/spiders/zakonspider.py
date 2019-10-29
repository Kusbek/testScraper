import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest
from ..items import TestprojectItem
import csv

class ZakonSpider(scrapy.Spider):
    name = "zakon"

    start_urls = [
        'https://zakon.kz/news'
    ]


    def parse(self, response):
        news_block = response.css("div#dle-content")
        all_news = news_block.css("div.cat_news_item")
        for news in all_news:
            href = news.css('a.tahoma::attr(href)').extract_first()
            if(href != None):
                url = 'https://zakon.kz'+href
                yield SplashRequest(url, callback=self.parseDetailedPage, errback=self.errback, dont_filter=True, args={'timeout': 60})
    
    def parseDetailedPage(self, response):
        comment_count = response.css("span.zknc-total-count::text").extract_first()
        comments = response.css("div.zknc-message::text").extract()
        date = response.css("span.news_date")
        day = date.css("::text").extract_first()
        time = date.css("span span::text").extract_first()

        items = TestprojectItem()
        title = response.css("h1::text").extract()
        story = response.css("div#initial_news_story p::text").extract()
        date = response.css("span.news_date")
        day = date.css("::text").extract_first()
        time = date.css("span span::text").extract_first()
        
        if(comment_count == None):
            comment_count = '0'
        items['title'] = title
        items['story'] = story
        if(day != None and time != None):
            items['date'] = day+time
        items['comment_count'] = comment_count
        items['comments'] = comments
        yield items
    def errback(self, failure):
        self.logger.info('Handled by the errback: %s (%s exception)', failure.request.url, str(failure.value))
        return {'url': failure.request.url}