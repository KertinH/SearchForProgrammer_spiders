# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from ..scrapy_redis.spiders import RedisSpider
from ..items import cnblog_qaItem
from ..Tools.md5 import get_md5

class CnblogsQandaSpider(RedisSpider):
    name = 'cnblogs_QA'
    allowed_domains = ['https://q.cnblogs.com/list/solved']
    # start_urls = ['https://q.cnblogs.com/list/solved']
    redis_key = 'cnblogs_QA:start_urls'

    def parse(self, response):
        data = response.xpath("//div[@class='left_sidebar']/div[@class='one_entity']/div[@class='news_item']")
        for title,content,tag,create_time,url in zip(
                data.xpath("h2/a/text()").extract(),
                data.xpath("div[@class='news_summary']/text()").extract(),
                data.xpath("div[@class='news_footer']/div[@class='question-tag-div']"),
                data.xpath("div[@class='news_footer']/div[@class='news_footer_user']/span/@title").extract(),
                data.xpath("h2/a/@href").extract()
        ):
            item = cnblog_qaItem()
            item['web_name'] = '博客园'
            item['web_url'] = 'https://www.cnblogs.com'
            item['title'] = title
            item['content'] = content
            item['tag'] = ','.join(tag.xpath("a/text()").extract())
            try:
                item['create_time'] = datetime.datetime.strptime(re.match('.*?([\d-]+).*',create_time).group(1),'%Y-%m-%d').date()
            except Exception as e:
                item['create_time'] = datetime.datetime.now().date()
            item['url'] = response.urljoin(url)
            item['url_md5'] = get_md5(item['url'])
            yield item
        if len(response.xpath("//div[@class='left_sidebar']/div[@id='pager']/a[contains(text(),'Next')]/@href").extract()) > 0:
            next_page = response.xpath("//div[@class='left_sidebar']/div[@id='pager']/a[contains(text(),'Next')]/@href").extract_first()
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)
        pass
    
