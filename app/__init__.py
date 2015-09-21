#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 16:30

@my_story __init__.py.py

@author : OmegaMiao"""


import logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config
from flask.ext.mail import Mail


loginManager = LoginManager()
loginManager.session_protection = 'strong'

app = Flask(__name__)
app.config.from_object(config['dev'])
db = SQLAlchemy(app)
loginManager.init_app(app)

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
logger = app.logger
logger.addHandler(console)
logger.setLevel(logging.DEBUG)

# mail
mail = Mail(app)

from controller import app
from models import Author, Story, Category
