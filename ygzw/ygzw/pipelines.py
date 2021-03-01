from itemadapter import ItemAdapter
from ygzw.items import YgzwItem
import logging
import csv
logger = logging.getLogger(__name__)

class YgzwPipeline:
    def __init__(self):
        self.f = open("./通知公告.csv","a+",newline='',encoding='utf8')
        self.writer = csv.writer(self.f)
        self.writer.writerow(['标题','日期','发布人','内容'])
        

    def process_item(self, item, spider):
        if isinstance(item,YgzwItem):
            logger.warning(item)
            self.writer.writerow([item['title'],item['date'],item['author'],item['content']])
        return item
    
    def close_spider(self,spider):
        self.f.close()
