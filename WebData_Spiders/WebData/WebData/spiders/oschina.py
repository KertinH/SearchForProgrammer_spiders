# -*- coding: utf-8 -*-
import scrapy
import re
import time
import datetime
import pytz
from ..scrapy_redis.spiders import RedisSpider
from ..items import oschinaItem
from ..Tools.md5 import get_md5
from ..settings import all_id


class OschinaSpider(RedisSpider):
    name = 'oschina'
    allowed_domains = ['https://www.oschina.net/question?catalog=1']
    # start_urls = ['https://www.oschina.net/question?catalog=1&show=updated&p=1']
    redis_key = 'oschina:start_urls'
    count = 1

    def parse(self, response):
        if len(response.xpath("//section[@class='question_list']/article[@class='wrapper question-wrapper ']/section/div[@class='box-fl question_counts']/"
                              "ul[@class='box']/li[@class='answer answered answer-accepted']").extract()) > 0:
            data = response.xpath("//section[@class='question_list']/article[@class='wrapper question-wrapper ']/section/div[@class='box-fl question_counts']/"
                                  "ul[@class='box']/li[@class='answer answered answer-accepted']/../../../div[@class='box-aw question_detail']")
            for title,content,tag,create_time,url in zip(
                    data.xpath("header/a/h4/text()").extract(),
                    data.xpath("section/text()").extract(),
                    data.xpath("footer"),
                    [i for i in data.xpath("footer/span/text()").extract() if i != '\n                                '],
                    data.xpath("header/a/@href").extract()
            ):
                item = oschinaItem()
                item['web_name'] = '开源中国'
                item['web_url'] = 'https://www.oschina.net'
                item['title'] = title
                item['content'] = content
                item['tag'] = ','.join(tag.xpath("div[@class='tooltipstered']/a/text()").extract())
                clock = int(re.match('^\n.*?([\d]+).*',create_time).group(1))
                if '小时' in create_time:
                    item['create_time'] = datetime.datetime.strptime(datetime.datetime.fromtimestamp(int(int(time.time())-clock*60*60),
                                                                                                     pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d'),'%Y-%m-%d').date()
                if '天' in create_time:
                    item['create_time'] = datetime.datetime.strptime(datetime.datetime.fromtimestamp(int(int(time.time())-clock*24*60*60),
                                                                                                     pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d'),'%Y-%m-%d').date()
                if '周' in create_time:
                    item['create_time'] = datetime.datetime.strptime(datetime.datetime.fromtimestamp(int(int(time.time())-clock*7*24*60*60),
                                                                                                     pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d'),'%Y-%m-%d').date()
                if '月' in create_time:
                    item['create_time'] = datetime.datetime.strptime(datetime.datetime.fromtimestamp(int(int(time.time())-clock*30*24*60*60),
                                                                                                     pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d'),'%Y-%m-%d').date()
                if '年' in create_time:
                    item['create_time'] = datetime.datetime.strptime(datetime.datetime.fromtimestamp(int(int(time.time())-clock*365*24*60*60),
                                                                                                     pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d'),'%Y-%m-%d').date()
                item['url'] = url
                item['url_md5'] = get_md5(url)
                if item['url_md5'] in all_id:
                    break
                yield item
            if self.count < 3124 and item['url_md5'] not in all_id:
                self.count += 1
                next_url = 'https://www.oschina.net/question?catalog=1&show=updated&p={}'.format(self.count)
                yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)
            else:
                print('oschina爬取结束')
                yield scrapy.Request('https://stackoverflow.com/questions?page=1&sort=newest',callback=self.parse,dont_filter=True)
        else:
            if self.count < 3124:
                self.count += 1
                next_url = 'https://www.oschina.net/question?catalog=1&show=updated&p={}'.format(self.count)
                yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)
