# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    author_id=scrapy.Field()
    nickname=scrapy.Field()
    released_at=scrapy.Field()
    promote_intro=scrapy.Field()
    tag_id = scrapy.Field()
    tag_title=scrapy.Field()
    likes_count=scrapy.Field()
    comments_count=scrapy.Field()
    keywords=scrapy.Field()
    content=scrapy.Field()
    banner=scrapy.Field()
    article_id=scrapy.Field()

class AuthorItem(scrapy.Item):
    nickname=scrapy.Field()
    avatar=scrapy.Field()
    bio=scrapy.Field()
    liked_count=scrapy.Field()
    all_words_count=scrapy.Field()
    attention_count=scrapy.Field()
    followed_count=scrapy.Field()
    author_id=scrapy.Field()
    articles_count=scrapy.Field()

class CommentItem(scrapy.Item):
    comments=scrapy.Field()
    released_at=scrapy.Field()
    likes_count=scrapy.Field()
    unlikes_count=scrapy.Field()
    user_id=scrapy.Field()
    comment_id=scrapy.Field()

class DictionaryItem(scrapy.Item):
    title=scrapy.Field()
    dic_kind=scrapy.Field()
    dic_id=scrapy.Field()


