# SearchForProgrammer_spiders
## SearchForProgrammer（爬虫模块）
## 爬取六个国内外知名编程类问答网站的问答模块数据，并存入elasticsearch（包括搜索建议及分词）
## pipelines内提供数据的mysql异步插入
#### CSDN、Stack Overflow、开源中国、segmentFault、treehouse、博客园
### 框架：
#### scrapy、scrapy-redis
### 库：
#### datetime
#### time
#### pytz
#### re
#### sys
#### os
#### setuptools
#### twisted
#### MYSQLdb
#### elasticsearch_dsl
#### random
#### redis
#### hashlib
<br></br>
## 更新(2018.4.7)：
### 加入（投机取巧型）增量爬取功能
### 加入（我都不好意思说的）暂停爬虫的数据存储文件夹
#### 如需中间暂停，启动爬虫命令更改为(spidername=爬虫名，yourFileName=随意命名的文件)：
    启动：scrapy crawl spidername -s JOBDIR=StorageProcess/yourFileName
    
    暂停：Ctrl+C
    
    重启：scrapy crawl spidername -s JOBDIR=StorageProcess/yourFileName(与启动命令相同)
