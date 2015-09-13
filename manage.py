#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/13 11:23

@my_story manage.py

@author : OmegaMiao"""


from flask.ext.script import Manager, Server
from app import app


manager = Manager(app)
manager.add_command("runserver", Server(host='127.0.0.1', port=5000, use_debugger=True))


if __name__ == '__main__':
    manager.run()
