#!/usr/bin/env python
# -*- coding=utf-8 -*-

import webapp2
from google.appengine.api import mail
from models import Page

class MailWorkHandler(webapp2.RequestHandler):
    """
    MailWorkHandler, send mail.
    """

    def get(self):
        p = Page.get_by_id(pid)

        tmp_content = jinja_template('sigle_page.html', { 'item': p };

        mail.send_mail(sender = fromAddr,
            to = toAddr,
            subject = subj,
            body = "deliver from ReadLater, by tonychi",
            attachments=[("%s.html" % p.title, tmp_content)])
    # end get

#end MailWorkHandler

class FeedWorkHandler(webapp2.RequestHandler):
    """
    FeedHandler, fetch feed with given feed id.
    """

    def get(self):
        pass

    # end get

# end FeedWorkHandler

app = webapp2.WSGIApplication([
    ('/work/mail', MailWorkHandler),
    ('/work/feed', FeedWorkHandler)
], debug=True)

