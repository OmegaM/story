#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/13 17:11

@my_story demo.py

@author : OmegaMiao"""


from app import app, db
from config import config
from app.models import Story, Category, Author
from flask import url_for


pages = Story.query.order_by(Story.create_time.desc()).paginate(5, 1, error_out=False)

for i in pages.iter_pages(left_edge=2, left_current=1, right_current=1, right_edge=3):
    print i, pages.page

print Category.query.get(1)

print Author.query.filter(Author.nick_name == 'Steven Gerrard').one().storys[0].title
print Category.query.filter(Category.name == 'Java').one().storys[0].content
