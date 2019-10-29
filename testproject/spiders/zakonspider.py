import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest
from ..items import TestprojectItem
import csv

class ZakonSpider(scrapy.Spider):
    name = "zakon"
    #Starting url
    start_urls = [
        'https://zakon.kz/news'
    ]

    #parsing initial news catalog page, where we obtain list of all recent news
    def parse(self, response):
        news_block = response.css("div#dle-content")
        all_news = news_block.css("div.cat_news_item") # exctracting all hrefs
        for news in all_news:
            href = news.css('a.tahoma::attr(href)').extract_first()
            if(href != None):
                url = 'https://zakon.kz'+href 
                yield SplashRequest(url, callback=self.parseDetailedPage, errback=self.errback, dont_filter=True, args={'timeout': 60}) #sending request for detailed page
    #parsing detailed page
    def parseDetailedPage(self, response):
        comment_count = response.css("span.zknc-total-count::text").extract_first() #number of comments
        comments = response.css("div.zknc-message::text").extract()#list of all comments without parent children relation, too cumborsome to do
        date = response.css("span.news_date")
        day = date.css("::text").extract_first()#publciation DD.Month.YYYY
        time = date.css("span span::text").extract_first()#publication time
        #saving into items from items.py

        title = response.css("h1::text").extract()#news title
        story = response.css("div#initial_news_story p::text").extract()#shallow parsing of news body, hard to find a pattern to follow
        items = TestprojectItem()
        #handling no comments
        if(comment_count == None):
            comment_count = '0'
        items['title'] = title
        items['story'] = story
        #some pages are different
        if(day != None and time != None):
            items['date'] = day+time
        items['comment_count'] = comment_count
        items['comments'] = comments
        yield items
    
    def errback(self, failure):
        self.logger.info('Handled by the errback: %s (%s exception)', failure.request.url, str(failure.value))
        return {'url': failure.request.url}