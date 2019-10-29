import scrapy
#Here is our model for each extacted page
class TestprojectItem(scrapy.Item):

    story = scrapy.Field()
    date = scrapy.Field()
    comment_count = scrapy.Field()
    title = scrapy.Field()
    comments = scrapy.Field()
    pass
