BOT_NAME = 'testproject'

SPIDER_MODULES = ['testproject.spiders']
NEWSPIDER_MODULE = 'testproject.spiders'




# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# PROXY_POOL_ENABLED = True
# PROXY_POOL_PAGE_RETRY_TIMES = 10

SPLASH_URL = 'http://localhost:8050'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'




ITEM_PIPELINES = {
    'testproject.pipelines.TestprojectPipeline': 500,
}
DOWNLOADER_MIDDLEWARES = {
#     'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
#     'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
#    'testproject.middlewares.TestprojectSpiderMiddleware': 543,
}

