#!/usr/bin/env python
# -*- coding=utf-8 -*-

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

class MainHandler(BaseHandler):
    """ all pages using pageit """

    def get(self):
        q = Page.all();
        q.order('-insertTime')
        its = q.fetch(10, 0)
        render_template('index.html', { 'title': 'List', 'items': its })

class ViewHandler(BaseHandler):
    """ per page """

    def get(self, pid):
        itId = int(pid)
        p = db.get(db.Key.from_path('Page', itId))
        render_template('view.html', { 'title': p.title, 'item': p })

class DeleteHandler(BaseHandler):
    """ delete page """

    def get(self, pid):
        itId = int(pid)
        p = db.get(db.Key.from_path('Page', itId))
        db.delete(p)
        return webapp2.redirect('/')

class SendHandler(BaseHandler):
    """ send already exist item """

    def sendIt(subj, toAddr, page):
        html = template('view.html', { 'title': page.title, 'item': page })
        filename = page.title + '.html'

        msg = EmailMessage(sender="qiwei219@gmail.com", subject=subj, to=toAddr);
        msg.attachments = [(filename, html)]
        msg.send()

    def get(self, pid):
        itId = int(pid)
        p = db.get(db.Key.from_path('Page', itId))

        sendIt('convert', 'qiwei219_72@kindle.com')

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write('{ successed:true, id:%s }' % p.key().id())

class SendDirectHandler(SendHandler):
    """ receive save request, and send mail to it """

    def options(self):
    """
    http://stackoverflow.com/questions/298745/how-do-i-send-a-cross-domain-post-request-via-javascript#answer-7605119
    http://wuyuntao.blogspot.com/2008/12/jquery-douban-greasemonkey.html
    http://webapp-improved.appspot.com/guide/request.html?highlight=header
    http://www.codeotaku.com/journal/2011-05/cross-domain-ajax/index#1
    http://www.firefox.net.cn/dig/api/gm_xmlhttprequest.html
    """
        h = self.request.headers['HTTP_ORIGIN']
        if h == 'http://getpocket.com' or h == 'https://getpocket.com':
            response.headers['Access-Control-Allow-Origin'] = self.request.headers['HTTP_ORIGIN']
            response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
            response.headers['Access-Control-Max-Age'] = '1000'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    def post(self):
        #表单字段： url, author, title, content, allow_sendto_kindle
        b = self.request.get('allow_sendto_kindle')
        p = Page(url = self.request.get('url'), 
                 author = self.request.get('author'),
                 title = self.request.get('title'),
                 content = self.request.get('content'))
        p.put(); # save

        # send to kindle
        if b: sendIt('convert', 'qiwei219_72@kindle.com', p)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write('{ successed:true, id:%s }' % p.key().id())

