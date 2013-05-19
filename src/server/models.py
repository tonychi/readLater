#!/usr/bin/env python
# -*- coding=utf-8 -*-

from google.appengine.ext import db

class Feed(db.Model):
    title = db.stringProperty()
    url = db.Linkproperty()
    interval = db.IntegerProperty(default=60*60*24)  # 1day
    fetchTime = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def allowFetch(cls, _id, time):
        ''' 检查指定Feed的最后检查时间是否大于time+Feed.interval‘'''
        it = Feed.get_by_id(_id)
        return True if it and (it.fetchTime - time).seconds > it.interval else False
    # end method
# end class

class Entry(db.Model):
    url = db.LinkProperty()
    title = db.StringProperty()
    author = db.StringProperty()
    content = db.TextProperty()
    tags = db.StringListProperty()
    insertTime = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def delete_by_id(cls, _id):
        ''' delete Entry by id '''
        it = Entry.get_by_id(_id)
        if it:
            it.delete()
    # end method
# end class
