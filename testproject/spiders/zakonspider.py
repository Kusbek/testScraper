import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest
from ..items import TestprojectItem
import csv
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

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
                yield SplashRequest(url, callback=self.parseDetailedPage, errback=self.errback_httpbin, dont_filter=True, args={'timeout': 60}) #sending request for detailed page
    #parsing detailed page
    def parseDetailedPage(self, response):
        comment_count = response.css("span.zknc-total-count::text").extract_first() #number of comments
        comments = response.css("div.zknc-message::text").extract()#list of all comments without parent children relation, too cumborsome to do
        date = response.css("span.news_date")
        day = date.css("::text").extract_first()#publciation DD.Month.YYYY
        time = date.css("span span::text").extract_first()#publication time
        

        title = response.css("h1::text").extract()#news title
        story = response.css("div#initial_news_story p::text").extract()#shallow parsing of news body, hard to find a pattern to follow
        #saving into items from items.py
        items = TestprojectItem()
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print(title)
        print("\n")
        print("\n")
        print("\n")
        
        if(title != []):
            # handling no comments
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
    
    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)