# -*- coding: utf-8 -*-
import scrapy
import datetime
import pytz
from ..scrapy_redis.spiders import RedisSpider
from ..items import segmentFaultItem
from ..Tools.md5 import get_md5
from ..settings import all_id


class SegmentfaultSpider(RedisSpider):
    name = 'sF'
    allowed_domains = ['https://segmentfault.com/questions?page=1']
    # start_urls = ['https://segmentfault.com/questions?page=1']
    redis_key = 'sF:start_urls'
    some = {}

    def parse(self, response):
        if len(response.xpath("//div[@class='stream-list question-stream']/section/div/div[@class='answers answered solved']/small/text()").extract()) > 0:
            data = response.xpath("//div[@class='stream-list question-stream']/section/div/div[@class='answers answered solved']/../../div[@class='summary']")
            for title,content,tag,url in zip(
                    data.xpath("h2/a/text()").extract(),
                    data.xpath("h2/a/text()").extract(),
                    data.xpath("ul[@class='taglist--inline ib']"),
                    data.xpath("h2/a/@href").extract()
            ):
                item = segmentFaultItem()
                item['web_name'] = 'SegmentFault'
                item['web_url'] = 'https://segmentfault.com'
                c_time = [response.xpath("//div[@class='stream-list question-stream']/section/div/div[@class='answers']/../../"
                                         "div[@class='summary']/ul[@class='author list-inline']/li/a/@data-created").extract_first()]
                item['title'] = title
                item['content'] = content
                tag = tag.xpath("li/a/text()").extract()
                r_tag = []
                for tag in tag:
                    r_tag.append(tag.replace('\n','').strip())
                item['tag'] = ','.join(r_tag)
                if c_time[0] != None:
                    item['create_time'] = datetime.datetime.strptime(datetime.datetime.fromtimestamp(int(c_time[0]),
                                                                        pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d'),'%Y-%m-%d').date()
                else:
                    item['create_time'] = datetime.datetime.now().date()
                item['url'] = response.urljoin(url)
                item['url_md5'] = get_md5(item['url'])
                self.some = item
                if item['url_md5'] in all_id:
                    break
                yield item
        if self.some:
            if len(response.xpath("//div[@class='text-center']/ul/li[@class='next']/a/@href").extract()) > 0 \
                    and self.some['url_md5'] not in all_id:
                next_page =  response.xpath("//div[@class='text-center']/ul/li[@class='next']/a/@href").extract_first()
                next_url = response.urljoin(next_page)
                yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)
            else:
                print('segmentFault爬取结束')
                yield scrapy.Request('https://segmentfault.com/questions?page=1',callback=self.parse,dont_filter=True)
        else:
            if len(response.xpath("//div[@class='text-center']/ul/li[@class='next']/a/@href").extract()) > 0:
                next_page = response.xpath("//div[@class='text-center']/ul/li[@class='next']/a/@href").extract_first()
                next_url = response.urljoin(next_page)
                yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
            pass
        pass
