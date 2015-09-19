#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 16:31

@my_story models.py

@author : OmegaMiao"""


from app import db
from datetime import datetime
from flask.ext.login import UserMixin


class Story(db.Model):
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return "<Story %r title %r>" % (self.id, self.title)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "create_time": self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    storys = db.relationship('Story', backref='category', lazy='joined')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category %r name %r>" % (self.id, self.name)


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    nick_name = db.Column(db.String(20), nullable=False, unique=True)
    storys = db.relationship('Story', backref='author', lazy='joined')

    def __init__(self, name, nick_name):
        self.name = name
        self.nick_name = nick_name

    def __repr__(self):
        return "<Author id: %r Name: %r nickName:%r>" % (self.id, self.name, self.nick_name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


if __name__ == '__main__':
    db.create_all()
