import scrapy
from ygzw.items import YgzwItem
import logging

logger = logging.getLogger(__name__)

class TzggSpider(scrapy.Spider):
    name = 'tzgg'
    allowed_domains = ['smzt.gd.gov.cn']
    start_urls = ['http://smzt.gd.gov.cn/zwgk/tzgg/index.html']

    def parse(self, response):
        info_list = response.xpath("//ul[@class='News_list']/li")
        item = YgzwItem()
        for info in info_list:
            item['title'] = info.xpath("./a/text()").extract_first()
            item['date'] = info.xpath("./span/text()").extract_first()
            detail_href = info.xpath("./a/@href").extract_first()
            yield scrapy.Request(
                url = detail_href,
                callback=self.parse_detail,
                meta={"item":item}
            )
        page_list = response.xpath("//div[@class='page']/a")
        for p in page_list:
            text = p.xpath("./text()").extract_first()
            if "下一页" in text:
                next_page = p.xpath("./@href").extract_first()
                yield scrapy.Request(
                    url = next_page,
                    callback=self.parse
                )
    
    def parse_detail(self,response):
        item = response.meta["item"]
        info = response.xpath("//div[@class='info_fbt']")
        item["author"] = info.xpath("./span[2]/text()").extract_first()
        item["content"] = response.xpath("//div[@id='zoomcon']/p/text()").extract_first()
        yield item