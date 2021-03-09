import scrapy
from dyspider.items import uservideoItem
import re
import json
import logging
import os
from copy import deepcopy

logger = logging.getLogger(__name__)

class UservideoSpider(scrapy.Spider):
    name = 'uservideo'
    allowed_domains = ['v.douyin.com','iesdouyin.com']
    start_urls = ['https://v.douyin.com/edWuvqY/']
    apiurl = "https://www.iesdouyin.com/web/api/v2/aweme/post"
    # ↓需要配置的变量
    _signature = "rJLGzwAAzOFESOSyb8OylaySxt"
    dytk = ""
    count = 25

    def parse(self, response):
        #获取重定向网址中的sec_uid
        pattern = re.compile("sec_uid=(.*?)&")
        sec_uid = re.findall(pattern,response.url)[0]
        url = self.apiurl+"?sec_uid="+sec_uid+"&_signature="+self._signature+"&dytk="+self.dytk+"&count="+str(self.count)
        yield scrapy.Request(
            url = url,
            method = 'GET',
            callback = self.parseDetail,
            dont_filter=True
        )
    
    '''
    处理返回的json数据
    '''
    def parseDetail(self,response):
        content = json.loads(response.text)
        awelist = content['aweme_list']
        logger.warning("视频个数:{}".format(len(awelist)))
        item = uservideoItem()
        #创建文件夹，以创作者名字命名
        self.author = awelist[0]["author"]["nickname"]
        if not os.path.isdir(self.author):
            os.makedirs(self.author)
        for d in awelist:
            item['author'] = self.author
            item['desc'] = d['desc']
            item['digg_count'] = d['statistics']['digg_count']
            item['comment_count'] = d['statistics']['comment_count']
            item['share_count'] = d['statistics']['share_count']
            item['videourl'] = d["video"]["play_addr"]["url_list"][0]
            yield item
            yield scrapy.Request(
                url = item['videourl'],
                method = 'GET',
                callback = self.downloadVideo,
                dont_filter = True,
                meta = {'item':deepcopy(item)}
            )
    
    def downloadVideo(self,response):
        item = response.meta['item']
        with open('{}/{}.mp4'.format(self.author,item['desc']),'wb') as f:
            f.write(response.body)
        logger.warning("视频《{}》下载完毕".format(item['desc']))


        
