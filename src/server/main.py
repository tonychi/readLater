#!/usr/bin/env python
# -*- coding=utf-8 -*-

import webapp2
import views

app = webapp2.WSGIApplication([
    ('/', views.MainHandler),
    ('/view/([\d]+)', views.ViewHandler),
    ('/delete/([\d]+)', views.DeleteHandler),
    ('/send/([\d]+)', views.SendHandler),
    ('/save', views.SendDirectHandler),
    ('/api/save', views.SendDirectHandler)
], debug=True)

