#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""Created with Pycharm IDEA

@Create on 2015/9/12 16:31

@my_story models.py

@author : OmegaMiao"""


from app import db, loginManager, logger
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
# import signature package
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


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
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        print current_app.config['SECRET_KEY']
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception, e:
            logger.error("load token data has an error, error message is ------> " + e.message)
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_STORY, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_STORY |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]  # add (Permission, )
            role.default = roles[r][1]  # add (, True or False)
            db.session.add(role)
        db.session.commit()


    def __repr__(self):
        return '<Role %r>' % self.name


class Permission:
    def __init__(self):
        pass

    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_STORY = 0x004
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
