from elasticsearch_dsl import DocType, Date, Completion, Keyword, Text
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as CA

connections.create_connection(hosts=['localhost'])


class CustomAnalyzer_(CA):
    '''实现Completion可传入analyzer=ik'''
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer_(filter_name='ik_max_word',filter = ['lowercase']) #lowercase处理大小写


class csdnQA_type(DocType):
    '''QA数据类型'''
    suggest = Completion(analyzer=ik_analyzer)
    web_name = Keyword()
    web_url = Keyword()
    title = Text(analyzer='ik_max_word')
    content = Text(analyzer='ik_max_word')
    tag = Text(analyzer='ik_max_word')
    create_time = Date()
    url = Keyword()
    url_md5 = Keyword()

    class Meta:
        index = 'qa'
        doc_type = 'csdn_qa'


class cnblogQA_type(csdnQA_type):
    class Meta:
        index = 'qa'
        doc_type = 'cnblog_qa'


class segmentFaultQA(csdnQA_type):
    class Meta:
        index = 'qa'
        doc_type = 'segmentfault_qa'


class stackOverflowQA(csdnQA_type):
    class Meta:
        index = 'qa'
        doc_type = 'stackoverflow_qa'


class oschinaQA(csdnQA_type):
    class Meta:
        index = 'qa'
        doc_type = 'oschina_qa'


class treehouseQA(csdnQA_type):
    class Meta:
        index = 'qa'
        doc_type = 'treehouse_qa'


if __name__ == "__main__":
    csdnQA_type.init()
    cnblogQA_type.init()
    segmentFaultQA.init()
    stackOverflowQA.init()
    oschinaQA.init()
    treehouseQA.init()
