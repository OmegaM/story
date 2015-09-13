#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 16:30

@my_story __init__.py.py

@author : OmegaMiao"""


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

app = Flask(__name__)
app.config.from_object(config['dev'])
db = SQLAlchemy(app)


from controller import app
from models import Author, Story, Category