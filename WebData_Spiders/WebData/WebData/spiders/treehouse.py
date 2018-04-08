# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from ..scrapy_redis.spiders import RedisSpider
from ..items import treehouseItem
from ..Tools.md5 import get_md5
from ..settings import all_id


class TreehouseSpider(RedisSpider):
    name = 'TH'
    allowed_domains = ['https://teamtreehouse.com/community']
    # start_urls = ['https://teamtreehouse.com/community']
    redis_key = 'treehouse:start_urls'
    some = {}

    def parse(self, response):
        if len(response.xpath("//ul[@class='discussion-list']/li[@class='discussion-item discussion-best-answer']").extract()) > 0:
            data = response.xpath("//ul[@class='discussion-list']/li[@class='discussion-item discussion-best-answer']/div[@class='discussion-meta']")
            for title,content,tag,create_time,url in zip(
                    data.xpath("h2/a/text()").extract(),
                    data.xpath("h2/a/text()").extract(),
                    data.xpath("ul"),
                    data.xpath("div/a/time/@datetime").extract(),
                    data.xpath("h2/a/@href").extract()
            ):
                item = treehouseItem()
                item['web_name'] = 'TreeHouse'
                item['web_url'] = 'https://teamtreehouse.com/community'
                item['title'] = title
                item['content'] = content
                item['tag'] = ','.join(tag.xpath("li/a/text()").extract())
                try:
                    item['create_time'] = datetime.datetime.strptime(re.match('.*?([\d-]+).*',create_time).group(1),'%Y-%m-%d').date()
                except Exception as e:
                    item['create_time'] = datetime.datetime.now().date()
                item['url'] = response.urljoin(url)
                item['url_md5'] = get_md5(item['url'])
                self.some = item
                if item['url_md5'] in all_id:
                    break
                yield item
        if self.some:
            if len(response.xpath("//div[@class='pagination-container']/a[contains(text(),'Next')]/@href").extract()) > 0\
                    and self.some['url_md5'] not in all_id:
                next_page = response.xpath("//div[@class='pagination-container']/a[contains(text(),'Next')]/@href").extract_first()
                next_url = response.urljoin(next_page)
                yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)
            else:
                print('treehouse爬取结束')
                yield scrapy.Request('https://teamtreehouse.com/community',callback=self.parse,dont_filter=True)
        else:
            if len(response.xpath("//div[@class='pagination-container']/a[contains(text(),'Next')]/@href").extract()) > 0:
                next_page = response.xpath("//div[@class='pagination-container']/a[contains(text(),'Next')]/@href").extract_first()
                next_url = response.urljoin(next_page)
                yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
            pass
        pass
