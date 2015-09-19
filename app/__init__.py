#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 16:30

@my_story __init__.py.py

@author : OmegaMiao"""


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config

loginManager = LoginManager()
loginManager.session_protection = 'strong'

app = Flask(__name__)
app.config.from_object(config['dev'])
db = SQLAlchemy(app)
loginManager.init_app(app)

from controller import app
from models import Author, Story, Category
