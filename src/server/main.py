#!/usr/bin/env python
# -*- coding=utf-8 -*-

import webapp2
import common
from models import Entry, Feed
import logging

logging.getLogger().setLevel(logging.DEBUG)

# /
class MainHandler(common.BaseHandler):
    """ all pages using pageit """

    def get(self):
        return self.redirect('/list/1')

PAGESIZE = 10 
# /list/([\d]+)
class ListHandler(common.BaseHandler):

    def get(self, pageindex):
        logging.info(pageindex)
        pi = 1 if int(pageindex) < 1 else int(pageindex)
        offset = (pi - 1) * PAGESIZE
        logging.info(offset)

        q = Entry.all();
        q.order('-insertTime')

        total = q.count()
        its = q.fetch(PAGESIZE, offset)

        self.render_template('index.html', { 
            'title': 'Entry List', 'items': its, 'total': total, 
            'pageindex': pi, 'pagesize': PAGESIZE })

# /view/([\d]+)
class ViewHandler(common.BaseHandler):
    """ per page """

    def get(self, pid):
        itId = int(pid)
        p = Entry.get_by_id(itId)
        self.render_template('view.html', { 'title': p.title, 'item': p })

# /delete/([\d]+)
class DeleteHandler(common.BaseHandler):
    """ delete page """

    def get(self, pid):
        itId = int(pid)
        Entry.delete_by_id(itId)
        return self.redirect('/list/1')

# /send/
class SendHandler(common.BaseHandler):
    """ send already exist item """

    def post(self):
        """ add task to mail queue """

        title = self.request.get('title')
        pid = self.request.get('pid')

        user = 1
        t = title if title else 'NEWS'

        common.add_task_sendmail(user, t, pid)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write('{ "success": True }')

# /save
class SendDirectHandler(common.BaseHandler):
    """ receive save request, and send mail to it 
    get请求返回send.html页面，包含提交表单。可以作为公布给终端用户的UI
    post请求支持保存和发送两个操作，如果用户勾选了同时发送到kindle的话会自动发送出去 
    """

    def get(self):
        """ render send.html """
        self.render_template('save.html', { 'title': 'New Entry' })

    def post(self):
        #表单字段： url, author, title, content, allow_sendto_kindle
        bSendIt = self.request.get('bSendIt')

        p = Entry()
        p.url = self.request.get('tUrl')
        p.author = self.request.get('tAuthor')
        p.title = self.request.get('tTitle')
        p.content = self.request.get('tContent')
        p.tags = self.request.get('tTags').split(',')
        p.put(); # save

        #send to kindle
        if bSendIt: 
            common.add_task_sendmail(p.key().id());

        return self.redirect('/list/1')

class FeedListHandler(common.BaseHandler):
    def get(self):
        q = Feed.all();
        its = q.fetch(limit=100)

        self.render_template('feed.html', { 'title': 'Feed List', 'items': its })

class FeedSaveHandler(common.BaseHandler):
    def get(self):
        self.render_template('feed_save.html', { 'title': 'New Feed' })

    def post(self):
        #表单字段： url, author, title, content, allow_sendto_kindle
        f = Feed()
        f.url = self.request.get('tUrl')
        f.title = self.request.get('tTitle')
        f.put(); # save

        return self.redirect('/feed')

# create app, define url route.
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/list/([\d]+)', ListHandler),
    ('/view/([\d]+)', ViewHandler),
    ('/delete/([\d]+)', DeleteHandler),
    ('/send', SendHandler),
    ('/save', SendDirectHandler),
    ('/feed', FeedListHandler),
    ('/feed/save', FeedSaveHandler),
], debug=True)

