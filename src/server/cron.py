#!/usr/bin/env python
# -*- coding=utf-8 -*-

import webapp2
import logging
from models import Feed
from common import add_task_fetchfeed, add_task_sendmail

logging.getLogger().setLevel(logging.DEBUG)

class FeedCronHandler(webapp2.RequestHandler):
    """
    FeedCronHandler, 处理Feed抓取工作
    """

    def get(self, time):
        """
        GET请求处理。
        从当前用户的订阅列表内抓取一定数量的Feed，放入抓取队列内。
        """
        logging.debug(time)

        feeds = Feed.get_by_interval(int(time))

        logging.debug('feed count: %s', len(feeds))

        for fit in feeds:
            # add to task queue
            add_task_fetchfeed(fit.key().id(), fit.url)
        # end for

    # end get
# end FeedCronHandler

class MailCronHandler(webapp2.RequestHandler):
    """
    """

    def get(self):
        pass

    # end get

# end MailCronHandler

app = webapp2.WSGIApplication([
    ('/cron/feed/([\d]+)', FeedCronHandler),
    ('/cron/mail', MailCronHandler)
], debug=True)

