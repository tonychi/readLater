#!/usr/bin/env python
# -*- coding=utf-8 -*-

import webapp2
from google.appengine.api import mail
from models import Page
from datetime import datetime

TIMEZONE = 8

class MailWorkHandler(webapp2.RequestHandler):
    """
    MailWorkHandler, send mail.
    """

    def get(self, user, title, pids):
        """ user: 用户id
        title: 文件名，文件内容标题
        pids: 文章列表
        """

        pages, idx = [], 1

        tmp_pids = pids.split(',')

        if tmp_pids:
            for it in tmp_pids:
                tmp_page = Page.get_by_id(int(it))
                tmp = { \
                        'idx': idx, \
                        'title': p.title, \
                        'author': p.author, \
                        'url': p.url, \
                        'tags': ','.join(p.tags), \
                        'content': p.content \
                    }
                pages.append(tmp)
                idx += 1
            # end for
        # end if

        tmp_content = jinja_template('ebook_pages.html', { \ 
                    'title': title, \
                    'createTime': datetime.utcnow() + timedelta(hours=TIMEZONE)) \
                    'pages': pages \
                })

        user_addr = 'qiwei219_72@kindle.com'

        mail.send_mail(to = user_addr, \
            subject = 'Convert', \
            body = "deliver from READ LATER, By Tony Chi", \
            attachments=[("%s.html" % .title, tmp_content)])

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

