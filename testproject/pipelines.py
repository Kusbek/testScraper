from scrapy.exporters import CsvItemExporter

#pipeline for saving output into zakon.csv
class TestprojectPipeline(object):
    def __init__(self):
        self.file = open("zakon.csv", 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()        

    def process_item(self, item, spider):
        self.exporter.export_item(item)   
        return item
       