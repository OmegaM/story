#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/21 22:28

@my_story sendemail.py

@author : OmegaMiao"""


from flask.ext.mail import Message
from flask import render_template
from threading import Thread
from app import mail, app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    msg = Message('[Omega]' + subject, sender='miaolei51886666@126.com', recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
