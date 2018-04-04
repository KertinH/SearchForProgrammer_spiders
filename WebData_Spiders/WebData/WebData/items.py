# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from .es_models.types import csdnQA_type,cnblogQA_type,segmentFaultQA,stackOverflowQA,oschinaQA,treehouseQA
from elasticsearch_dsl.connections import connections
import scrapy

es = connections.create_connection(csdnQA_type._doc_type.using)

def gen_suggests(index,info_tumple):
    '''根据字符串生成搜索建议数组'''
    used_words = set()
    suggests = []
    for text,weight in info_tumple:
        if text:
            #调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index,params={'analyzer':'ik_max_word','filter':['lowercase']},body=text)
            analyzed_words = set([r['token'] for r in words['tokens'] if len(r['token']) > 1])
            new_words = analyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({'input':list(new_words),'weight':weight})

    return suggests

class WebdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class csdn_qaItem(scrapy.Item):
    web_url = scrapy.Field()
    web_name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    tag = scrapy.Field()
    create_time = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field()

    def insert(self):
        insert = '''
            insert into csdn_qa(title,web_name,content,tag,create_time,url,url_md5,web_url)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        param = (self['title'],self['web_name'],self['content'],self['tag'],self['create_time'],self['url'],self['url_md5'],self['web_url'])
        return insert,param

    def saveToEs(self):
        webData = csdnQA_type()
        webData.web_url = self['web_url']
        webData.web_name = self['web_name']
        webData.title = self['title']
        webData.content = self['content']
        webData.tag = self['tag']
        webData.create_time = self['create_time']
        webData.url = self['url']
        webData.meta.id = self['url_md5']
        webData.suggest = gen_suggests(csdnQA_type._doc_type.index,((webData.title,10),(webData.tag,7)))
        webData.save()

        return


class cnblog_qaItem(scrapy.Item):
    web_url = scrapy.Field()
    web_name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    tag = scrapy.Field()
    create_time = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field()

    def insert(self):
        insert = '''
            insert into cnblog_qa(title,web_name,content,tag,create_time,url,url_md5,web_url)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        param = (self['title'],self['web_name'],self['content'],self['tag'],self['create_time'],self['url'],self['url_md5'],self['web_url'])
        return insert,param

    def saveToEs(self):
        webData = cnblogQA_type()
        webData.web_name = self['web_name']
        webData.web_url = self['web_url']
        webData.title = self['title']
        webData.content = self['content']
        webData.tag = self['tag']
        webData.create_time = self['create_time']
        webData.url = self['url']
        webData.meta.id = self['url_md5']
        webData.suggest = gen_suggests(cnblogQA_type._doc_type.index, ((webData.title, 10), (webData.tag, 7)))
        webData.save()

        return


class stackOverflowItem(scrapy.Item):
    web_url = scrapy.Field()
    web_name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    tag = scrapy.Field()
    create_time = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field()

    def insert(self):
        insert = '''
            insert into stackOverflow(title,web_name,content,tag,create_time,url,url_md5,web_url)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        param = (self['title'],self['web_name'],self['content'],self['tag'],self['create_time'],self['url'],self['url_md5'],self['web_url'])
        return insert,param

    def saveToEs(self):
        webData = stackOverflowQA()
        webData.web_name = self['web_name']
        webData.web_url = self['web_url']
        webData.title = self['title']
        webData.content = self['content']
        webData.tag = self['tag']
        webData.create_time = self['create_time']
        webData.url = self['url']
        webData.meta.id = self['url_md5']
        webData.suggest = gen_suggests(stackOverflowQA._doc_type.index, ((webData.title, 10), (webData.tag, 7)))
        webData.save()

        return


class segmentFaultItem(scrapy.Item):
    web_url = scrapy.Field()
    web_name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    tag = scrapy.Field()
    create_time = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field()

    def insert(self):
        insert = '''
            insert into segmentFault(title,web_name,content,tag,create_time,url,url_md5,web_url)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        param = (self['title'],self['web_name'],self['content'],self['tag'],self['create_time'],self['url'],self['url_md5'],self['web_url'])
        return insert,param

    def saveToEs(self):
        webData = segmentFaultQA()
        webData.web_name = self['web_name']
        webData.web_url = self['web_url']
        webData.title = self['title']
        webData.content = self['content']
        webData.tag = self['tag']
        webData.create_time = self['create_time']
        webData.url = self['url']
        webData.meta.id = self['url_md5']
        webData.suggest = gen_suggests(segmentFaultQA._doc_type.index, ((webData.title, 10), (webData.tag, 7)))
        webData.save()

        return


class oschinaItem(scrapy.Item):
    web_url = scrapy.Field()
    web_name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    tag = scrapy.Field()
    create_time = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field()

    def insert(self):
        insert = '''
            insert into oschina(title,web_name,content,tag,create_time,url,url_md5,web_url)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        param = (self['title'],self['web_name'],self['content'],self['tag'],self['create_time'],self['url'],self['url_md5'],self['web_url'])
        return insert,param

    def saveToEs(self):
        webData = oschinaQA()
        webData.web_name = self['web_name']
        webData.web_url = self['web_url']
        webData.title = self['title']
        webData.content = self['content']
        webData.tag = self['tag']
        webData.create_time = self['create_time']
        webData.url = self['url']
        webData.meta.id = self['url_md5']
        webData.suggest = gen_suggests(oschinaQA._doc_type.index, ((webData.title, 10), (webData.tag, 7)))
        webData.save()

        return


class treehouseItem(scrapy.Item):
    web_url = scrapy.Field()
    web_name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    tag = scrapy.Field()
    create_time = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field()

    def insert(self):
        insert = '''
            insert into treehouse(title,web_name,content,tag,create_time,url,url_md5,web_url)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        param = (self['title'],self['web_name'],self['content'],self['tag'],self['create_time'],self['url'],self['url_md5'],self['web_url'])
        return insert,param

    def saveToEs(self):
        webData = treehouseQA()
        webData.web_name = self['web_name']
        webData.web_url = self['web_url']
        webData.title = self['title']
        webData.content = self['content']
        webData.tag = self['tag']
        webData.create_time = self['create_time']
        webData.url = self['url']
        webData.meta.id = self['url_md5']
        webData.suggest = gen_suggests(treehouseQA._doc_type.index, ((webData.title, 10), (webData.tag, 7)))
        webData.save()

        return
