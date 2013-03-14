#!/usr/bin/env python
# -*- coding=utf-8 -*-

from google.appengine.ext import db

class Page(db.Model):
    url = db.LinkProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    insertTime = db.DateTimeProperty(auto_now_add=True)

