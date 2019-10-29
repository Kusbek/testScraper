# Test Scraper
This test task is the web crawler for [zakon.kz/news](zakon.kz/news)

In order to bypass proxy block uncomment lines 12,13 30, 31 in settings.py

If you want obey rules of robot.txt change
``` ROBOTTXT_OBEY = False -> True  ```

p.s zakon.kz would not work if you obey the rules

to run the scrapper write following command in project directory

>$scrapy crawl zakon

output file is pipelined into "zakon.csv"

