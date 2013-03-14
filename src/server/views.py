#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Last Change:  2013-03-14 10:51:56

import os
import webapp2
import jinja2
from google.appengine.ext import db
from models import Page

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

class BaseHandler(webapp2.RequestHandler):
    """ define template method, use jinja2 """

    def template(self, view, values, **args):
        """ return string """
        tpl = jinja_env.get_template(view)
        return tpl.render(values)

    def render_template(self, view, data, **args):
        """ direct wirte to out stream """
        self.response.out.write(template(view, data, args))

# /
class MainHandler(BaseHandler):
    """ all pages using pageit """

    def get(self):
        q = Page.all();
        q.order('-insertTime')
        its = q.fetch(10, 0)
        render_template('index.html', { 'title': 'List', 'items': its })

# /view/([\d]+)
class ViewHandler(BaseHandler):
    """ per page """

    def get(self, pid):
        itId = int(pid)
        p = db.get(db.Key.from_path('Page', itId))
        render_template('view.html', { 'title': p.title, 'item': p })

# /delete/([\d]+)
class DeleteHandler(BaseHandler):
    """ delete page """

    def get(self, pid):
        itId = int(pid)
        p = db.get(db.Key.from_path('Page', itId))
        db.delete(p)
        return webapp2.redirect('/')

# /send/([\d]+)
class SendHandler(BaseHandler):
    """ send already exist item """

    def sendIt(subj, toAddr, page):
        html = template('view.html', { 'title': page.title, 'item': page })
        filename = page.title + '.html'

        msg = EmailMessage(sender="qiwei219@gmail.com", subject=subj, to=toAddr);
        msg.attachments = [(filename, html)]
        msg.send()

    def post(self, pid):
        itId = int(pid)
        p = db.get(db.Key.from_path('Page', itId))

        sendIt('convert', 'qiwei219_72@kindle.com')

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write('{ successed:true, id:%s }' % p.key().id())

# /save
class SendDirectHandler(SendHandler):
    """ receive save request, and send mail to it 
    get请求返回send.html页面，包含提交表单。可以作为公布给终端用户的UI
    post请求支持保存和发送两个操作，如果用户勾选了同时发送到kindle的话会自动发送出去 
    """

    def get(self):
        """ render send.html """
        render_template('send.html', { 'title': 'Send' })

    def post(self):
        #表单字段： url, author, title, content, allow_sendto_kindle
        bSendIt = self.request.get('bSendIt')
        p = Page(url = self.request.get('tUrl'), 
            author = self.request.get('tAuthor'),
            title = self.request.get('tTitle'),
            content = self.request.get('tContent'),
            tags = self.request.get('tTags'))
        p.put(); # save

        #send to kindle
        if bSendIt: 
            mail = self.request.get('tMail')
            sendIt('convert', mail, p)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write('{ successed:true, id:%s }' % p.key().id())

