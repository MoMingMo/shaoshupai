import scrapy
import json
from shaoshupai.items import ArticleItem,DictionaryItem,AuthorItem,CommentItem

class shaoshupaiSpider(scrapy.Spider):
    name = 'shaoshupai'
    limit=10
    offset=0
    total=0
    allowed_domains = ['https://sspai.com/']
    start_urls = ['https://sspai.com/api/v1/articles?offset={0}&limit={1}&include_total=true'.format(offset,limit)]
    
    def parse(self, response):
        print('list_url='+response.url)
        result=json.loads(response.body)
        data=result.get('list')
        self.total=result.get('total')#总数
        i=0
        for item in data:
            i+=1
            self.tags=item.get('tags')
            self.topics=item.get('topics')
            print('第{0}条文章{1}------{2}'.format((self.offset*self.limit+i),item.get('title'),item.get('id')))
            #文章详情
            url='https://sspai.com/post/{0}'.format(item.get('id'))
            #文章前一百条评论
            comment_url='https://sspai.com/api/v1/comment/user/article/hot/page/get?limit=100&offset=0&article_id={0}&user_id=0'.format(item.get('id'))
            meta={
                 'article_id':item.get('id'),
                 'title':item.get('title'),
                 'released_at':item.get('released_at'),
                 'author_id':item.get('author').get('id'),
                 'nickname':item.get('author').get('nickname'),
                 'tag_title':item.get('tag_title'),
                 'promote_intro':item.get('summary'),
                 'tag_id': [tag_id for tag_id in self.tags],
                 'likes_count':item.get('likes_count'),
                 'comments_count':item.get('comments_count'),
                 'keywords':item.get('keywords'),
                 'banner':item.get('banner')
            }
            yield scrapy.Request(url,meta=meta,callback=self.article_detail,dont_filter = True)
            yield scrapy.Request(url='https://sspai.com/api/v1/users/{0}'.format(item.get('author').get('id')),callback=self.article_author,dont_filter = True)
            yield scrapy.Request(url=comment_url,callback=self.article_comments,dont_filter=True)
            yield scrapy.Request(url,callback=self.article_tags,dont_filter = True)
            yield scrapy.Request(url,callback=self.article_topics,dont_filter = True)
       
        
        self.offset+=10
        if self.offset*self.limit<=self.total:
            list_url='https://sspai.com/api/v1/articles?offset={0}&limit={1}&include_total=true'.format(self.offset,self.limit)
            yield scrapy.Request(url=list_url,callback=self.parse,dont_filter=True)
        pass
     #标签   
    def article_tags(self,response):
        for item in self.tags:
            tag=DictionaryItem()
            tag['dic_kind']=1
            tag['dic_id']=item.get('id')
            tag['title']=item.get('title')
            yield tag
        #topic
    def article_topics(self,response):
        for item in self.topics:
            topic=DictionaryItem()
            topic['dic_kind']=0
            topic['dic_id']=item.get('id')
            topic['title']=item.get('title')
            yield topic
    #作者信息
    def article_author(self,response):
        item=json.loads(response.body)
        author=AuthorItem()
        author['nickname']=item.get('nickname')
        author['avatar']=item.get('avatar')
        author['bio']=item.get('bio')
        author['liked_count']=item.get('liked_count')
        author['all_words_count']=item.get('articles_word_count')
        author['attention_count']=item.get('following_count')
        author['followed_count']=item.get('followed_count')
        author['author_id']=item.get('id')
        author['articles_count']=item.get('articles_count')
        yield author

    #文章详情
    def article_detail(self, response):
        print('url='+response.url+'----------'+str(response.meta['article_id']))
        item=ArticleItem()
        item['article_id']=response.meta['article_id']
        item['title']=response.meta['title']
        item['author_id']=response.meta['author_id']
        item['nickname']=response.meta['nickname']
        item['released_at']=response.meta['released_at']
        item['promote_intro']=response.meta['promote_intro']
        item['tag_id']=','.join([str(x.get('id')) for x in response.meta['tag_id']])
        item['tag_title']=','.join([str(x.get('title')) for x in response.meta['tag_id']])  
        item['likes_count']=response.meta['likes_count']
        item['comments_count']=response.meta['comments_count']
        item['keywords']=','.join(response.meta['keywords'])
        item['banner']=response.meta['banner']
        item['content']=response.css('#article-content > div').extract_first()
        yield item
    #文章评论
    def article_comments(self,response):
        comments=json.loads(response.body).get('data')
        # if not comments:
        for item in comments:
            comment=CommentItem()
            comment['comments']=item.get('comment')
            comment['released_at']=item.get('created_at')
            comment['likes_count']=item.get('likes_count')
            comment['unlikes_count']=item.get('unlikes_count')
            comment['user_id']=item.get('user').get('id')
            comment['comment_id']=item.get('id')
            yield comment