from itemadapter import ItemAdapter
from dyspider.items import uservideoItem
import openpyxl

class DyspiderPipeline:
    def __init__(self):
        self.workbook = openpyxl.Workbook()
        self.worksheet = self.workbook.active
        self.worksheet.append(['简介','点赞量','评论量','分享量'])
        self.author = ''
    
    def process_item(self, item, spider):
        if isinstance(item,uservideoItem):
            self.worksheet.append([item['desc'],item['digg_count'],item['comment_count'],item['share_count']])
            if self.author == '':
                self.author = item['author']
        return item
    
    def close_spider(self,spider):
        self.workbook.save('{}/{}.xlsx'.format(self.author,self.author))
