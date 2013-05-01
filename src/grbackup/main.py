#!/usr/bin/env python
# -*- coding=utf-8 -*-

'''
import urllib2

proxies = {"http": "http://%s" % "127.0.0.1:8087" }
proxy_support = urllib2.ProxyHandler(proxies)
opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler(debuglevel=1))
urllib2.install_opener(opener)
'''

from mongoengine import *
import libgreader as libgr
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG, 
        format='%(asctime)s:%(msecs)03d %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M')

class Category(Document):
    cid = StringField(required=True)
    label = StringField(required=True)

class Feed(Document):
    fid = StringField(required=True)
    title = StringField(required=True)
    url = URLField(required=True)
    site = URLField()
    categories = ListField(ReferenceField(Category, dbref=True))

class Entry(Document):
    title = StringField(required=True)
    url = URLField(required=True)
    author = StringField()
    content = StringField(required=True)
    createdTime = DateTimeField()
    feed = ReferenceField(Feed, dbref=True)
    tags = ListField(StringField(max_length=30))

USER = 'qiwei219@gmail.com'
PWD = 'magxiluffgqtorgd'
DB = 'greader'

logging.debug('loading ....')

_auth = libgr.ClientAuthMethod(USER, PWD)
_reader = libgr.GoogleReader(_auth)

logging.debug('login')

def init():
    '''
    初始化greader的基础数据，‘
    '''
    logging.debug('begin init...')

    #user = _reader.getUserInfo()
    _reader.buildSubscriptionList()

    logging.debug('build subscriptions ok.')

    logging.debug('----------')
    categories = _reader.getCategories()
    _dic_categories = {}
    for c in categories:
        tmpC = Category(cid=c.id, label=c.label)
        tmpC.save()
        _dic_categories[tmpC.cid] = tmpC
        logging.debug('add category, %s, %s', tmpC.cid, tmpC.label)

    logging.debug('----------')
    feeds = _reader.getFeeds()
    for f in feeds:
        tmpF = Feed(fid=f.id,
                title=f.title,
                url=f.feedUrl,
                site=f.siteUrl,
                categories= [_dic_categories[c.id] for c in f.categories])
        tmpF.save()
        logging.debug('add feed, %s, %s, %s', tmpF.fid, tmpF.title, tmpF.url)

    logging.debug('end init...')

FETCH_LIMIT = 40

#import time
#import math
#UNTIL = str(int(time.mktime(datetime(2012,2,9).timetuple())))
UNTIL = None 

def fetch_feed(feeds):
    logging.debug('begin fetch feeds')

    for f in feeds:
        logging.debug("+++++++++++++")
        logging.debug("do fetch, %s", f)

        tmpF = Feed.objects(fid=f)[0]  #find it by id
        grFeed = libgr.Feed(_reader, tmpF.title, tmpF.fid)
        result = _reader.getFeedContent(grFeed, loadLimit=FETCH_LIMIT, 
                until=UNTIL)
        do_continue(tmpF, grFeed, result)

        logging.debug("-------------")

    logging.debug('end fetch feeds')

def do_continue(tmpF, feed, result):

    id = result.get('id', '')
    key = result.get('continuation', '')
    items = result.get('items', [])

    logging.debug("----->>>>>");
    logging.debug("do_continue, %s, %s", id, key)

    if items:
        for it in items:
            tmpE = Entry(feed = tmpF,
                    title = it.get('title', ''),
                    author = it.get('author', '(no author)'))

            if tmpE.title == '':
                logging.warning('title is empty')
                continue
                    
            #parse publish date
            pd = it.get('published', '')
            pd = pd if pd != '' else it.get('updated', '')
            if pd:
                tmpE.createdTime = datetime.fromtimestamp(pd)

            #parse url
            for alt in it.get('alternate', []):
                if alt.get('type', '') == 'text/html':
                    tmpE.url = alt.get('href', '')
                    break

            if tmpE.url == None:
                tmpE.url = 'http://not-found.com'

            #parse content
            content = it.get('content', it.get('summary', {}))
            if content:
                tmpE.content = content.get('content', '')
            else:
                print it.get('content') 
                tmpE.content = '(no content)'

            tmpE.save()

            logging.debug("add Entry, %s, %s", tmpE.title, tmpE.createdTime)
        # end for
    # enf if

    logging.debug("-----<<<<<")

    if key:
        logging.debug("---- execute next continuation-----")
        nextResult = _reader.getFeedContent(feed, 
                continuation=key, loadLimit=FETCH_LIMIT, until=UNTIL)
        do_continue(tmpF, feed, nextResult)

if __name__ == '__main__':

    connect(DB)
    #init()

    feeds = [
        ##'feed/http://blog.codingnow.com/atom.xml',
        ##'feed/http://blog.zhaojie.me/rss',
        ##'feed/http://coolshell.cn/?feed=rss2',
        ##'feed/http://www.cnblogs.com/huangxincheng/rss',
        ##'feed/http://www.ruanyifeng.com/blog/atom.xml',
        ##'feed/http://blog.jobbole.com/feed/',
        ##'feed/http://www.cnblogs.com/artech/rss',
        ##'feed/http://feed.feedsky.com/iamsujie',
        ##'feed/http://blog.sina.com.cn/rss/1228571733.xml',
        ##'feed/http://feeds.feedburner.com/hc1983',
        ##'feed/http://songshuhui.net/feed'
    ]
    fetch_feed(feeds)

