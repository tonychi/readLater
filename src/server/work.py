#!/usr/bin/env python
# -*- coding=utf-8 -*-

import webapp2
from google.appengine.api import mail
#from google.appengine.api import users
#from google.appengine.api import memcache
#from google.appengine.api import urlfetch
from datetime import datetime, timedelta
from models import Entry
import common

TIMEZONE = 8

class MailWorkHandler(webapp2.RequestHandler):
    """
    MailWorkHandler, send mail.
    """

    def get(self):
        """ user: 用户id
        title: 文件名，文件内容标题
        pids: 文章列表
        """
        user, title, pids = self.request.get('user'), \
                self.request.get('title'), \
                self.request.get('pids')

        pages, idx = [], 1

        tmp_pids = pids.split(',')

        if tmp_pids:
            for it in tmp_pids:
                tmp_page = Entry.get_by_id(int(it))
                tmp = { 
                    'idx': idx, 
                    'title': tmp_page.title, 
                    'author': tmp_page.author, 
                    'time': tmp_page.insertTime,
                    'url': tmp_page.url, 
                    'tags': ", ".join(tmp_page.tags), 
                    'content': tmp_page.content 
                }
                pages.append(tmp)
                idx += 1
            # end for
        # end if

        tmp_content = common.jinja_template('ebook_pages.html', { 
                'title': title, 
                'createTime': datetime.utcnow() + timedelta(hours=TIMEZONE),
                'pages': pages 
            })

        sender_addr = 'Tony <qiwei219@gmail.com>'
        user_addr = 'qiwei219_72@kindle.com'

        mail.send_mail(sender = sender_addr, \
            to = user_addr, \
            subject = 'Convert', \
            body = "deliver from READ LATER, By Tony Chi", \
            attachments=[("%s.html" % title, tmp_content)])

    # end get

#end MailWorkHandler

class FeedWorkHandler(webapp2.RequestHandler):
    """
    FeedHandler, fetch feed with given feed id.
    """

    def get(self, feed_url):
        pass

    # end get

# end FeedWorkHandler

app = webapp2.WSGIApplication([
    ('/work/mail', MailWorkHandler),
    ('/work/feed', FeedWorkHandler)
], debug=True)

