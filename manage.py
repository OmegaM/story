#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/13 11:23

@my_story manage.py

@author : OmegaMiao"""


from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import app, db
from app.models import User, Role


manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", Server(host='127.0.0.1', port=5000, use_debugger=True))
manager.add_command('db', MigrateCommand)  # add migrate command line

if __name__ == '__main__':
    manager.run()
