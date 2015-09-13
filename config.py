#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 18:01

@my_story config.py

@author : OmegaMiao"""


class Config(object):
    SQLALCHEMY_ECHO = True
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'

    def __init__(self):
        pass


class DevConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'mysql://root:wxhwbx6666@localhost/alchemy'


class TestConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'mysql://root:wxhwbx6666@localhost/story_test'


config = {
    'dev': DevConfig,
    'test': TestConfig
}
