# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
class TestprojectPipeline(object):
    def __init__(self):
        self.file = open("zakon.csv", 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()        

    def process_item(self, item, spider):
        # create_valid_csv(item)
        self.exporter.export_item(item)
        
        # def create_valid_csv(self, item):
        #     for key, value in item.items():
        #         is_string = (isinstance(value, basestring))
        #         if (is_string and ("," in value.encode('utf-8'))):
        #             item[key] = "\"" + value + "\""        
        return item