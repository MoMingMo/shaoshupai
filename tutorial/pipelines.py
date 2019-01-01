import pymysql
from scrapy import log

class TutorialPipeline(object):    
        def process_item(self, item, spider):
            #数据库链接
            con=pymysql.connect(host='localhost',user='root',passwd='YZM_root_123',db='BLOGDB',charset='utf8')
            #数据库游标
            cue=con.cursor()
            print("mysql connect succes")
            try:
                #获取文章内容 pymysql.escape_string转义内容
                content=pymysql.escape_string(str(item['content']))
                #SQL语句
                sqlstr = "insert into articles(title,time,author,content,articleid) VALUES('%s','%s','%s','%s','%s')"%(item['title'],item['time'],item['author'],content,item['articleid'])
                #执行SQL语句
                cue.execute(sqlstr)
            except Exception as e:
                print('Insert error:',e)
                #回滚
                con.rollback()
            else:
                #提交
                con.commit()
            #关闭链接
            con.close()


