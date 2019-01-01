import scrapy
import json
import requests
from scrapy import log
from tutorial.items import DmozItem

class DmozSpider(scrapy.spiders.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    offset=0 
    limit=50
    total=0
    start_urls = ["https://sspai.com/api/v1/articles?offset="+str(offset)+"&limit="+str(limit)+"&include_total=true"]

    def parse(self,response):
        #返回数据转json
        result = json.loads(response.body)  
        #获取总数
        self.total=result.get('total')
        #循环json中的list
        for data in result.get('list'):
            #获取文章id
            articleid=data.get('id')
            #回去文章发布时间
            time_span=data.get('released_at')
            #拼接详情页面地址
            url='https://sspai.com/post/'+str(articleid)+'' 
            log.msg('url='+url,log.INFO)
            #详情 
            # meta 给回调函数传递参数
            yield scrapy.Request(url,meta={'articleid':articleid,'time_span':time_span},callback=self.getdatail,dont_filter = True)
        #翻页
        self.offset=self.offset+1
        #判断是否继续翻页
        if self.offset*self.limit<=self.total:
            #拼接新的列表页面
            satrt_url='https://sspai.com/api/v1/articles?offset='+str(self.offset)+'&limit='+str(self.limit)+''
            log.msg('satrt_url='+satrt_url,log.INFO)
            #回调自己形成循环
            yield scrapy.Request(url=satrt_url,callback=self.parse,dont_filter = True)
    #处理文章详情        
    def getdatail(self, response):
         #通过 response.meta['xxx']获取参数
         #文章id
         articleid=response.meta['articleid']
         #发布时间
         time_span=response.meta['time_span']
         #提取页面相关内容
         for sel in response.xpath('//*[@id="app"]/div/div[1]/div/div[2]'):
            item= DmozItem()
            item['title'] = sel.xpath('//*[@id="app"]/div/div[1]/div/div[2]/div/article/h1/text()').extract_first()
            item['time']=time_span
            item['author']=sel.xpath('//*[@id="app"]/div/div[1]/div/div[2]/div/article/div[1]/div[2]/h4/a/text()').extract_first()
            item['content']=sel.xpath('//*[@id="article-content"]/div').extract()
            item['articleid']=articleid
            yield item 