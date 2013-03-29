#!/usr/bin/env python
# -*- coding=utf-8 -*-

from google.appengine.ext import db

class Page(db.Model):
    url = db.LinkProperty()
    title = db.StringProperty()
    author = db.StringProperty()
    content = db.TextProperty()
    tags = db.StringListProperty()
    insertTime = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def delete_by_id(cls, _id):
        it = Page.get_by_id(_id);
        if it:
            it.delete()

    # end method

# end class
