#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import webapp2
import jinja2
from models import Page

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

def datetime(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)

jinja_env.filters['datetime'] = datetime

def jinja_template(view, values):
    """ 
    extend method: jinja_template, return string.
    """

    tpl = jinja_env.get_template(view)
    return tpl.render(values)

class BaseHandler(webapp2.RequestHandler):
    """ define template method, use jinja2 """

    def render_template(self, view, data):
        """ direct wirte to out stream """
        self.response.out.write(jinja_template(view, data))

def sendMail(subj, content, toAddr, page):
    """
    extend method: send e-mail 
    """

    mail.send_mail(sender = mail_sender,
              to = user.kindle_email,
              subject = "Convert",
              body = "deliver from ReadLater, by tonychi",
              attachments=[("%s.html" % title, content)])

    html = jinja_template('view.html', { 'title': page.title, 'item': page })
    filename = page.title + '.html'

    msg = EmailMessage(sender="qiwei219@gmail.com", subject=subj, to=toAddr);
    msg.attachments = [(filename, html)]
    msg.send()

def new_queue_name(queue, count=0):
    """docstring for get_queue_name"""

    if count <= 0:
        return queue
    else:
        return "%s-%s" % (queue, random.randint(0, count))

def add_task_sendmail(user, pid):
    """
    添加发送邮件任务，只传入Pageid, UserId.
    任务自己来处理邮件内容构建, 邮件接收人的信息通过UserInfo获得.
    """

    taskqueue.add(url='/work/mail', 
            queue_name = new_queue_name("mail-queue"),
            method = 'GET',
            params = { 'user': user, 'pid': pid })

def add_task_fetchfeed(feed_url):
    """
    添加检查Feed更新的任务，传入Feedid。
    """

    taskqueue.add(url='/work/feed', 
            queue_name = new_queue_name("feed-fetch-queue"),
            method = 'GET',
            params = { 'feed_url': feed_url })

