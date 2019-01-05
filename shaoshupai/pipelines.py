from pymysql import cursors 
from scrapy import log
import base64
from shaoshupai.items import ArticleItem,DictionaryItem,AuthorItem,CommentItem
import traceback
import sys
from twisted.enterprise import adbapi
import copy

class ShaoshupaiPipeline(object):
     def __init__(self,dbpool):
       self.dbpool=dbpool
     @classmethod
     def from_settings(cls,settings):
         params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset=settings['MYSQL_CHARSET'],
            port=settings['MYSQL_PORT'],
            cursorclass=cursors.DictCursor,
         # host='localhost',
         # db='BlogDB',
         # user='root',
         # passwd='YZM_root_123',
         # charset='utf8',
         # port='3306',
         # cursorclass=cursors.DictCursor,
         )
         dbpool = adbapi.ConnectionPool('pymysql', **params)
         return cls(dbpool)
      #  self.conn= pymysql.connect(host='localhost',user='root',password='YZM_root_123',db='BlogDB',charset='utf8')
      #  self.cursor=self.conn.cursor()
     def process_item(self, item, spider):
            asynItem = copy.deepcopy(item)
            # 使用twisted将MySQL插入变成异步执行
            query = self.dbpool.runInteraction(self.insert_db, asynItem)
            # 添加异常处理
            query.addCallback(self.handle_error)
            pass
     def handle_error(self, failure):
            # 处理异步插入时的异常
        log.msg(failure,log.ERROR)
     def insert_db(self, cursor, item):
         try:
             sql=""
             if isinstance(item,DictionaryItem):
                # print('写入dictionary表')
                sql+="INSERT INTO ssp_dictionary(title,kind,_id)VALUES('%s','%s','%s')"%(item['title'],item['dic_kind'],item['dic_id'])
             elif isinstance(item,AuthorItem):
                # print('写入author表')
                bio=base64.b64encode((item['bio']).encode('utf8')).decode('utf8')
                all_words_count="0"
                attention_count="0"
                followed_count="0"
                if not item['all_words_count'] is None:
                   all_words_count=item['all_words_count']
                if not item['attention_count'] is None:
                    attention_count=item['attention_count']
                if not item['followed_count'] is None:
                    followed_count=item['followed_count']
                sql+="INSERT INTO ssp_author(nickname,avatar,bio,liked_count,all_words_count,attention_count,followed_count,author_id,articles_count) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(item['nickname'],item['avatar'],bio,item['liked_count'],all_words_count,attention_count,followed_count,item['author_id'],item['articles_count'])
             elif isinstance(item,ArticleItem):
                print('写入article表'+str(item['article_id']))
                content=""
                promote_intro=""
                if not item['promote_intro'] is None:
                   promote_intro=base64.b64encode((item['promote_intro']).encode('utf8')).decode('utf8')
                if not item['content'] is None:
                   content=base64.b64encode((item['content']).encode('utf8')).decode('utf8')   
                
                sql+="INSERT INTO ssp_article(title,author_id,nickname,released_at,promote_intro,tag_id,tag_title,likes_count,comments_count,keywords,content,banner,article_id) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(item['title'],item['author_id'],item['nickname'],item['released_at'],promote_intro,item['tag_id'],item['tag_title'],item['likes_count'],item['comments_count'],item['keywords'],content,item['banner'],item['article_id'])
             else:
                #  print('写入评论表')
                 comments=base64.b64encode((item['comments']).encode('utf8')).decode('utf8')   
                 sql+="INSERT INTO ssp_comments(comments,released_at,pick_count,tread_count,user_id,comment_id)VALUE('%s','%s','%s','%s','%s','%s')" %(comments,item['released_at'],item['likes_count'],item['unlikes_count'],item['user_id'],item['comment_id'])
             cursor.execute(sql)
         except Exception as ex:
                 ex_type, ex_val, ex_stack = sys.exc_info()
                 log.msg('{0},{1},{2},{3}'.format(ex,ex_type,ex_val,ex_stack),log.ERROR)
         else:
             pass
