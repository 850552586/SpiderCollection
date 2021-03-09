import scrapy


class DyspiderItem(scrapy.Item):
    pass


'''
用户视频item
'''
class uservideoItem(scrapy.Item):
    #作者
    author = scrapy.Field()
    #点赞量
    digg_count = scrapy.Field()
    #评论量
    comment_count = scrapy.Field()
    #分享量
    share_count = scrapy.Field()
    #视频简介
    desc = scrapy.Field()
    #视频地址
    videourl = scrapy.Field()
