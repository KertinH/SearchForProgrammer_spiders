# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from ..scrapy_redis.spiders import RedisSpider
from ..items import csdn_qaItem
from ..Tools.md5 import get_md5
from ..settings import all_id


class CsdnQandaSpider(RedisSpider):
    name = 'csdn_QA'
    allowed_domains = ['http://ask.csdn.net/questions?type=resolved']
    # start_urls = ['http://ask.csdn.net/questions?type=resolved']
    redis_key = 'csdn_QA:start_urls'
    some = {}

    def parse(self, response):
        data = response.xpath("//div[@class='common_con clearfix']/div[@class='questions_detail_con']")
        for title,content,tag,create_time,url in zip(
            data.xpath("dl/dt/a/text()").extract(),
            data.xpath("dl/dd/text()").extract(),
            data.xpath("div[@class='tags']"),
            data.xpath("div[@class='q_time']/span/text()").extract(),
            data.xpath("dl/dt/a/@href").extract()
        ):
            item = csdn_qaItem()
            item['web_name'] = 'CSDN'
            item['web_url'] = 'https://www.csdn.net'
            item['title'] = title
            item['content'] = content
            item['tag'] = ','.join(tag.xpath("a/text()").extract())
            try:
                item['create_time'] = datetime.datetime.strptime(re.match('.*?([\d.]+).*',create_time).group(1),'%Y.%m.%d').date()
            except Exception as e:
                item['create_time'] = datetime.datetime.now().date()
            item['url'] = url
            item['url_md5'] = get_md5(url)
            self.some = item
            if item['url_md5'] in all_id:
                break
            yield item
        if self.some:
            if len(response.xpath("//div[@class='common_con clearfix']/div[@class='csdn-pagination hide-set']/span/a[contains(text(),'下一页')]").extract()) > 0 \
                    and self.some['url_md5'] not in all_id:
                next_page = response.xpath("//div[@class='common_con clearfix']/div[@class='csdn-pagination hide-set']/span/a[contains(text(),'下一页')]/./@href").extract_first()
                next_url = response.urljoin(next_page)
                yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)
            else:
                print('csdn爬取结束')
                yield scrapy.Request('http://ask.csdn.net/questions?type=resolved',callback=self.parse,dont_filter=True)
        else:
            if len(response.xpath("//div[@class='common_con clearfix']/div[@class='csdn-pagination hide-set']/span/a[contains(text(),'下一页')]").extract()) > 0:
                next_page = response.xpath("//div[@class='common_con clearfix']/div[@class='csdn-pagination hide-set']/span/a[contains(text(),'下一页')]/./@href").extract_first()
                next_url = response.urljoin(next_page)
                yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
            pass
        pass
