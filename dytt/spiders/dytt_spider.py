# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DyttItem

class DyttSpiderSpider(CrawlSpider):
    name = 'dytt_spider'
    allowed_domains = ['dytt8.net']
    start_urls = ['http://www.dytt8.net/html/gndy/dyzz/list_23_1.html']

    rules = (
        Rule(LinkExtractor(allow=r'.+list_23_\d+\.html'),follow=True),
        Rule(LinkExtractor(allow=r'.+html\/gndy\/dyzz\/20\d+\/\d+.html'),callback="parse_detail",follow=False),
    )

    def parse_detail(self, response):
        movie = DyttItem()
        title = response.xpath("//h1//text()").get()
        movie['title'] = title
        imgs = response.xpath("//div[@id='Zoom']//img/@src").getall()

        if len(imgs) >= 2:
            cover = imgs[0]
            screenshot = imgs[1]
        else:
            cover = imgs[0]
            screenshot = ""
        movie['cover'] = cover
        movie['screenshot'] = screenshot

        # 定义一个解析info的函数
        def parse_info(info, value):
            return info.replace(value, "").strip()

        # # 数据进行清洗和过滤
        infos = response.xpath("//div[@id='Zoom']//text()").getall()
        for index, info in enumerate(infos):
            if info.startswith('◎译　　名'):
                # print(info.replace('◎译　　名',"").strip())
                movie['name'] = parse_info(info, '◎译　　名')
            elif info.startswith('◎产　　地'):
                info = parse_info(info, '◎产　　地')
                movie['city'] = info
            elif info.startswith('◎类　　别'):
                movie['category'] = parse_info(info, '◎类　　别')

            elif info.startswith('◎导　　演'):
                movie['director'] = parse_info(info, '◎导　　演')

            # 一行数据就是这个列表的一个元素，因此对索引进行判断，判断索引所在的列表元素是否是符合的内容！
            elif info.startswith('◎主　　演'):
                info = parse_info(info, '◎主　　演')
                actors = [info]
                for i in range(index + 1, len(infos)):
                    if infos[i].startswith('◎'):
                        break
                    actors.append(infos[i].strip())
                movie['actors'] = actors
            elif info.startswith('◎'):
                profile = []
                for i in range(index + 1, len(infos)):
                    if not infos[i].startswith('【'):
                        profile.append(infos[i].strip())
                    else:
                        break
                movie['profile'] = profile[0]
        yield movie
