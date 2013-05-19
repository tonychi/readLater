#!/usr/bin/env python
# -*- coding=utf-8 -*-

from google.appengine.ext import db
from datetime import timedelta, time

class Feed(db.Model):
    title = db.StringProperty()
    url = db.LinkProperty()
    interval = db.IntegerProperty(default=60*60*24)  # 1day
    lastedPublishedTime = db.DateTimeProperty()
    fetchTime = db.DateTimeProperty(auto_now_add=True)

    def is_allow_fetch(self, dt):
        ''' 检查指定Feed的最后检查时间是否大于time+Feed.interval‘'''
        '''
        t0 = self.fetchTime + timedelta(seconds=self.interval)
        t1 = time.mktime(t0.timetuple()).time()
        t2 = time.mktime(dt.timetuple()).time()
        return True if t1 >= t2 else Flase
        '''
        return True
        # return True if (self.fetchTime - time).seconds >= self.interval else False

    @classmethod
    def get_by_interval(cls, value):
        q = Feed.all()
        q.filter('interval', value)
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

