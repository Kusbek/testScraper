import scrapy
from scrapy.http import Request
from ..items import TestprojectItem

class ZakonSpider(scrapy.Spider):
    name = "zakon"
    start_urls = [
        'http://zakon.kz/news'
    ]

    def parse(self, response):
        news_block = response.css("div#dle-content")
        all_news = news_block.css("div.cat_news_item")
        for news in all_news:
            href = news.css('a.tahoma::attr(href)').extract_first()
            if(href != None):
                url = 'https://www.zakon.kz'+href
                yield Request(url, callback=self.parseDetailedPage, dont_filter=True)
    
    def parseDetailedPage(self, response):
        items = TestprojectItem()
        title = response.css("h1::text").extract()
        story = response.css("div#initial_news_story p::text").extract()
        date = response.css("span.news_date")
        day = date.css("::text").extract_first()
        time = date.css("span span::text").extract_first()
        comment_count = response.css("span.zknc-total-count::text").extract_first()
        items['title'] = title
        items['story'] = story
        items['date'] = day+time
        items['comment_count'] = comment_count
        filename = 'zakon.csv'
        yield items