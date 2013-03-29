#!/usr/bin/env python
# -*- coding=utf-8 -*-

import webapp2
from common import sendMail

class ItemHandler(webapp2.RequestHandler):
    """
    Item, 处理：
    - 查询Item列表, 支持分页，条件
    - 创建Item
    """

    def get(self):
        """
        /api/item, GET, query, return first page
        /api/item?offset=20, GET, query, return offset pages
        /api/item?qt=QueryTerm, GET, query, user query terms.
        """
        pass
    
    def post(self):
        """
        /api/item, POST, create item 
        表单字段： url, author, title, content
        """

        p = Page()
        p.url = self.request.get('tUrl')
        p.author = self.request.get('tAuthor')
        p.title = self.request.get('tTitle')
        p.content = self.request.get('tContent')
        p.tags = self.request.get('tTags').split(',')
        p.put(); # save

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write('{ "success":true, "id":%s }' % p.key().id())

class ItemSignleHandler(webapp2.RequestHandler)
    """
    Item, 处理: 
    - 查询指定<key>的Item.
    - 更新指定<key>的Item内容.
    - 删除指定<key>的Item.
    """

    def get(self, key):
        """
        /api/item/<key>, GET, query specifed item
        """
        pass

    def put(self, key):
        """
        /api/item/<key>, PUT, update or replace specifed item
        """
        pass

    def delete(self, key)
        """
        /api/item/<key>, DELETE, delete specifed item with given <key>
        """
        pass

# create app, define url route.
app = webapp2.WSGIApplication([
    ('/api/item', ItemHandler),
    ('/api/item/([\d]+)', ItemSignleHandler)
], debug=True)

