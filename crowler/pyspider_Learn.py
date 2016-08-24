#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-08-23 20:04:42
# Project: v2exdemo

from pyspider.libs.base_handler import *
import random
import MySQLdb


class Handler(BaseHandler):
    crawl_config = {
         'headers' : {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'www.v2ex.com',
            'If-None-Match':'W/"8022fbf1c2e635aa7aa6b361c19408a020a5113c"',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        }
    }
    
    def __init__(self):
        self.db = MySQLdb.connect('192.168.0.6', 'anboqing', 'password', 'wenda', charset='utf8')
    
    def add_question(self, title, content,avatarUrl,comments=None):
        try:
            cursor = self.db.cursor()
            sql = 'insert into question(title, content, user_id, created_date, comment_count) values ("%s","%s",%d, %s, 0)' % (title, content, random.randint(1, 10) , 'now()');
            cursor.execute(sql)
            lastRowId=int(cursor.lastrowid)
            
            if comments is not None:
                for comment in comments:
                    csql = 'insert into comment ( content,user_id,created_date,entity_id,entity_type,status) values ("%s","%d","%s","%d",1,0)' % (comment,random.randint(1,20),'now()',lastRowId)
                    print csql
                    cursor.execute(csql)
            self.db.commit()
        except Exception, e:
            print e
            self.db.rollback()

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.v2ex.com/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http://www.v2ex.com/?tab="]').items():
            self.crawl(each.attr.href, callback=self.tab_page)
     
    @config(priority=2)
    def tab_page(self, response):
        for each in response.doc('a[href^="http://www.v2ex.com/go/"]').items():
            self.crawl(each.attr.href, callback=self.board_page)

    @config(priority=2)
    def board_page(self, response):
        for each in response.doc('a[href^="http://www.v2ex.com/t/"]').items():
            url = each.attr.href
            if url.find('#reply')>0:
                url=url[0:url.find('#')]
            self.crawl(url, callback=self.detail_page)
        for each in response.doc('a.page_normal').items():
            self.crawl(url, callback=self.board_page)
            
    @config(priority=20)
    def detail_page(self, response):
        title=response.doc('h1').text()
        content=response.doc('div.topic_content').html()
        if content is not None:
            content=content.replace('"','\\"')
        else:
            content=' '
        avatarUrl = response.doc('div.cell img.avatar').attr.src
        if avatarUrl is not None:
            avatarUrl = avatarUrl[0:avatarUrl.find('?')]
        else:
            avatarUrl = 'http://cdn.v2ex.co/avatar/7bec/637a/163664_normal.png'
        #insert into db
        self.add_question(title,content,avatarUrl)
        
        #find all comments and insert into comment
        comments = response.doc('div.reply_content')
        if comments is not None:
            for each in comments.items():
                comment = each.html().replace('"','\\"')
                # add comment
                
        return {
            "url": response.url,
            "title": title,
            "content":content,
            "avatarUrl":avatarUrl,
            "comments":comments,
        }
