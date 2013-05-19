#!/usr/bin/env python
# -*- coding=utf-8 -*-

from google.appengine.ext import db

class Feed(db.Model):
    title = db.stringProperty()
    url = db.Linkproperty()
    interval = db.IntegerProperty(default=60*60*24)  # 1day
    lastedPublishedTime = db.DateTimeProperty()
    fetchTime = db.DateTimeProperty(auto_now_add=True)

    def is_allow_fetch(self, time):
        ''' 检查指定Feed的最后检查时间是否大于time+Feed.interval‘'''
        return True if (self.fetchTime - time).seconds >= self.interval else False

    @classmethod
    def get_by_interval(cls, value):
        q = Feed.all()
        q.filter('interval=', value)
        return q.fetch(limit=100)

class Entry(db.Model):
    url = db.LinkProperty()
    title = db.StringProperty()
    author = db.StringProperty()
    content = db.TextProperty()
    tags = db.StringListProperty()
    publishedTime = db.DateTimeProperty()
    insertTime = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def delete_by_id(cls, _id):
        ''' delete Entry by id '''
        it = Entry.get_by_id(_id)
        if it:
            it.delete()

