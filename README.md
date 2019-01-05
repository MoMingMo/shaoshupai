# 少数派文章爬取

> 爬取少数派首页文章列表、文章评论、作者信息等信息

``` bash
git clone git@github.com:yangziming22333/shaoshupai.git
cd shaoshupai
scrapy crawl shaoshupai
注意修改pipline中mysql数据库连接
表中都有做了唯一约束所以没有对数据进行去重处理

```
