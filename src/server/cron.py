#!/usr/bin/env python
# -*- coding=utf-8 -*-

import webapp2
from common import add_task_fetchfeed

class FeedCronHandler(webapp2.RequestHandler):
    """
    FeedCronHandler, 处理Feed抓取工作
    """

    def get(self):
        """
        GET请求处理。
        
        从当前用户的订阅列表内抓取一定数量的Feed，放入抓取队列内。

        筛选feed时，首先按最后抓取时间升序排列，取前20个。
        """

        # query top 20 feed
        feed = (1,2,3);

        for fit in feed:
            # add to task queue
            add_task_fetchfeed(fit.url)

            # update lasted fetch time

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
    ('/cron/feed', FeedCronHandler),
    ('/cron/mail', MailCronHandler)
], debug=True)

