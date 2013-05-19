#!/usr/bin/env python
# -*- coding=utf-8 -*-

import webapp2
import logging
import common
from google.appengine.api import mail
#from google.appengine.api import users
#from google.appengine.api import memcache
#from google.appengine.api import urlfetch
from datetime import datetime, timedelta
from models import Entry, Feed

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

import urllib2
import lib.feedparser as fd

class FeedWorkHandler(webapp2.RequestHandler):
    """
    FeedHandler, fetch feed with given feed id.
    """

    def get(self):

        feed_id, feed_url = self.request.get('feed_id'),
                self.request.get('feed_url')

        url_result = urllib2.urlopen(feed_url)
        feed_result = fd.parse(url_result)

        if feed_result.bozo == 1:
            logging.error('fetch error, id: %s, url: %s, error: %s', 
                    feed_id, feed_url, feed_result.bozo_exception)
            return

        feed_update_time = feed_result.get('updated', datetime.utcnow)
        has_update = True 

        f = Feed.get_by_id(feed_id)
        if f.is_allow_fetch(time):
            for entry in feed_result.entries:
                if entry.published_parsed <= f.lastedPublishedTime
                    logging.info('no updated, id: %s, url: %s' feed_id,
                            feed_url)
                    has_update = False
                    break

                e = Entry(title = entry.title,
                          url = entry.link,
                          author entry.author,
                          content = entry.content,
                          publishedTime = entry.published_parsed)
                e.put()
                logging.debug('fetch entry, url: %s', entry.link)
                          
        # update feed fetch time
        if has_update:
            f.lastedPublishedTime = feed_result.entries[0].published_parsed
        f.fetchTime = datetime.utcnow()
        f.put()

    # end get

# end FeedWorkHandler

app = webapp2.WSGIApplication([
    ('/work/mail', MailWorkHandler),
    ('/work/feed', FeedWorkHandler)
], debug=True)

