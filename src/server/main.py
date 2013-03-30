#!/usr/bin/env python
# -*- coding=utf-8 -*-

import webapp2
import common
from models import Page 

# /
class MainHandler(common.BaseHandler):
    """ all pages using pageit """

    def get(self):
        q = Page.all();
        q.order('-insertTime')
        its = q.fetch(10, 0)
        self.render_template('index.html', { 'title': 'List', 'items': its })

# /view/([\d]+)
class ViewHandler(common.BaseHandler):
    """ per page """

    def get(self, pid):
        itId = int(pid)
        p = Page.get_by_id(itId)
        self.render_template('view.html', { 'title': p.title, 'item': p })

# /delete/([\d]+)
class DeleteHandler(common.BaseHandler):
    """ delete page """

    def get(self, pid):
        itId = int(pid)
        Page.delete_by_id(itId)
        return webapp2.redirect('/')

# /send/([\d]+)
class SendHandler(common.BaseHandler):
    """ send already exist item """

    def post(self, title, pid):
        """ add task to mail queue """

        user = 1
        t = title if title else 'NEWS'

        add_task_sendmail(user, t, pid)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write('{ success:True, id:%s }' % p.key().id())

# /save
class SendDirectHandler(common.BaseHandler):
    """ receive save request, and send mail to it 
    get请求返回send.html页面，包含提交表单。可以作为公布给终端用户的UI
    post请求支持保存和发送两个操作，如果用户勾选了同时发送到kindle的话会自动发送出去 
    """

    def get(self):
        """ render send.html """
        self.render_template('save.html', { 'title': 'Save' })

    def post(self):
        #表单字段： url, author, title, content, allow_sendto_kindle
        bSendIt = self.request.get('bSendIt')

        p = Page()
        p.url = self.request.get('tUrl')
        p.author = self.request.get('tAuthor')
        p.title = self.request.get('tTitle')
        p.content = self.request.get('tContent')
        p.tags = self.request.get('tTags').split(',')
        p.put(); # save

        #send to kindle
        if bSendIt: 
            add_task_sendmail(p.key().id());

        return webapp2.redirect('/')

# create app, define url route.
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/view/([\d]+)', ViewHandler),
    ('/delete/([\d]+)', DeleteHandler),
    ('/send/([\d]+)', SendHandler),
    ('/save', SendDirectHandler),
], debug=True)

