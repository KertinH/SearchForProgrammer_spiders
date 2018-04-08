# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from ..scrapy_redis.spiders import RedisSpider
from ..items import stackOverflowItem
from ..Tools.md5 import get_md5
from ..settings import all_id


class StackoverflowSpider(RedisSpider):
    name = 'sO'
    allowed_domains = ['https://stackoverflow.com/questions?sort=newest']
    # start_urls = ['https://stackoverflow.com/questions?page=1&sort=newest']
    redis_key = 'sO:start_urls'

    def parse(self, response):
        if len(response.xpath("//div[@id='content']/div[@id='mainbar']/div[@id='questions']/div[@class='question-summary']/div[@class='statscontainer']"
                              "/div[2]/div[@class='status answered-accepted']").extract()) > 0:
            data = response.xpath("//div[@id='content']/div[@id='mainbar']/div[@id='questions']/div[@class='question-summary']/div[@class='statscontainer']"
                                   "/div[2]/div[@class='status answered-accepted']/../../../div[@class='summary']")
            for title,content,tag,create_time,url in zip(
                data.xpath("h3/a/text()").extract(),
                data.xpath("div[@class='excerpt']/text()").extract(),
                data.xpath("div[2]"),
                data.xpath("div[@class='started fr']/div[@class='user-info ']/div[@class='user-action-time']/span/@title").extract(),
                data.xpath("h3/a/@href").extract()
            ):
                item = stackOverflowItem()
                item['web_name'] = 'StackOverflow'
                item['web_url'] = 'https://stackoverflow.com/questions'
                item['title'] = title
                item['content'] = content
                item['tag'] = ','.join(tag.xpath("a[@class='post-tag']/text()").extract())
                try:
                    item['create_time'] = datetime.datetime.strptime(re.match('.*?([\d-]+).*', create_time).group(1),'%Y.%m.%d').date()
                except Exception as e:
                    item['create_time'] = datetime.datetime.now().date()
                item['url'] = response.urljoin(url)
                item['url_md5'] = get_md5(item['url'])
                if item['url_md5'] in all_id:
                    break
                yield item
        if len(response.xpath("//div[@id='content']/div[@id='mainbar']/div[@class='pager fl']/a/span[contains(text(),'next')]").extract()) > 0 \
                and item['url_md5'] not in all_id:
            next_page = response.xpath("//div[@id='content']/div[@id='mainbar']/div[@class='pager fl']/a/span[contains(text(),'next')]/../@href").extract_first()
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
        else:
            print('stackOverFlow爬取结束')
            yield scrapy.Request('https://stackoverflow.com/questions?page=1&sort=newest',callback=self.parse,dont_filter=True)
        pass
